from flow import Data_Packet,Ack_Packet,Router_Packet
from link import Link
from packet_tracker import PacketTracker
import clock
from event import Event, RoutingUpdateEvent
from event_queue import EventQueue
class Device:
	def __init__(self, id):
		self.id = id

	def attach_link(self, link):
		return

	def handle_packet(self, packet):
		return


class Host(Device):
	def __init__(self, id):
		Device.__init__(self, id)
		self.link = None
		self.flow = {}
		self.data_packet_tracker = {}
		self.event_scheduler = None
		self.flag=False
	def attach_link(self, link):
		if self.link == None:
			self.link = link

	def _data_received(self, packet):
		ack_tracker = self.flow[packet.flow_id].ack_tracker
		ack_tracker.handler(packet)
		return packet.send_ack_packet(ack_tracker.expect)   # send_ack!!!!

	def handle_packet(self, packet):
		if isinstance(packet, Data_Packet): # if it is a data packet, construct ack
			print "device:"+str(packet.id)
			#if(packet.id==5 and self.flag==False):
				#self.flag=not self.flag
				#return
			ack_packet = self._data_received(packet)
			self.link.send(ack_packet, self)
		elif isinstance(packet, Ack_Packet):    # if it is an ack, tell the flow that the ack has been received
			#print "ACK:"+str(packet.id)
			self.flow[packet.flow_id].receive_ack(packet)
		else:
			return

	def __str__(self):
		return "host: "+str(self.id)

	def send(self, packet):
		# assert packet.source = self
		self.link.send(packet, self)

	def send_routing_packet(self):
		#a = input(str(self.link.get_occupancy()))
		self.send(Router_Packet(self.link.get_occupancy() + 1, self, self.link, 64, clock.clk.get_time()))
		flag=False
		for f in self.flow:
			if(self.flow[f].ack_tracker.expect < self.flow[f].total_amount/1024):
				flag=True
		if(flag==True):
			print "expect " + str(self.flow[f].ack_tracker.expect) 
			self.link.scheduler.put_event(5, RoutingUpdateEvent(self))     # routing_update_period
		''''
		else:
            #a=input("send_finish")
			temp=self.link.scheduler
			self.link.scheduler=EventQueue(clock.clk.get_time())
			while (not temp.isEmpty()):
				(t,e)=temp.pop_event()
				if(not isinstance(e,RoutingUpdateEvent)):
					self.link.scheduler.add_event(t,e)
		'''





class RoutingTable:
	def __init__(self):
		self._table = {}
	
	def get_entry(self, device_id):
		if device_id in self._table:
			return self._table[device_id]  # device_id -> link, delay
		else:
			return None

	def set_up_table(self, id, link, delay):
		if id not in self._table:
			self._table[id] = (link, delay, 0)
			return True
		elif self._table[id][1] > delay: 
			#print "here"
			self._table[id] = (link, delay, 0)
			return True
		return False

	def __str__(self):
		for device_id in self._table:
			print str(device_id)+" "+str(self._table[device_id][0])+" "+str(self._table[device_id][1])+" "+str(self._table[device_id][2])
		return ""

# timestamp???
	def update_entry(self, id, link, delay, timestamp):
		if (timestamp > self._table[id][2]):
			self._table[id] = (link, delay, timestamp)
			return True
		else:
			return False

		'''if self._table[id][1] < 1.0:
			self._table[id] = (link, delay)
			return True
		elif self._table[id][1] > delay: 
			#print "here"
			self._table[id] = (link, delay)
			return True
		return False
		'''





class Router(Device):
	def __init__(self, id):
		Device.__init__(self, id)
		self.routing_table = RoutingTable()
		self.links = []
	
	def __str__(self):
		#return "Router ID  " + str(self.id) + "\n"
		print str(self.id)
		for link in self.links:
			print str(link.id)
		print
		return str(self.routing_table)+ "\n"
	
	
	def attach_link(self, link):
		self.links.append(link)
	
	def _handle_routing_packet(self, packet):
		if clock.clk.get_time() <= 4.5:	
			if self.routing_table.set_up_table(packet.source.id, packet.link, packet.delay) == True and packet.link in self.links:
				link_id = packet.link.id
				for att_link in self.links:
					if att_link.id != link_id:
						delay = self.routing_table.get_entry(packet.source.id)[1] + att_link.delay
						#print packet.source.id +" "+self.id +" "+link_id+" "+att_link.id + " "+str(packet.delay)
						#packet.link = att_link
						att_link.send(Router_Packet(delay, packet.source, att_link, 64, clock.clk.get_time()), self)
		else:
			if packet.source.id != self.id:
				if self.routing_table.update_entry(packet.source.id, packet.link, packet.delay, packet.time) == True and packet.link in self.links:
				#if self.routing_table.get_entry(packet.source.id)[1] != packet.delay:		
					link_id = packet.link.id
					for att_link in self.links:
						if att_link.id != link_id:
							delay = self.routing_table.get_entry(packet.source.id)[1] + att_link.get_occupancy() + 1
							att_link.send(Router_Packet(delay, packet.source, att_link, 64, packet.time), self)
							att_link.send(Router_Packet(att_link.get_occupancy() + 1, self, att_link, 64, packet.time), self)	
				'''
					link_id = packet.link.id
					for att_link in self.links:
						if att_link.id != link_id:
							delay = self.routing_table.get_entry(packet.source.id)[1] + att_link.get_occupancy() + 1
							att_link.send(Router_Packet(delay, packet.source, att_link, 64), self)
							att_link.send(Router_Packet(att_link.get_occupancy() + 1, self, att_link, 64), self)
				'''


	# update routing table


	# handle data packet or ack packet
	def _handle_data_ack_packet(self, packet):
		# looking up the routing table and forward the packet to next device
		link = self.routing_table.get_entry(packet.destination.id)[0]
		#print str(link.id) + " "+ str(packet.destination.id)

		link.send(packet, self)
		# what if destination not found in routing table?
	
	
	def handle_packet(self, packet):
		if isinstance(packet, Data_Packet) or isinstance(packet, Ack_Packet):
			self._handle_data_ack_packet(packet)
		elif isinstance(packet, Router_Packet):
			self._handle_routing_packet(packet)




if __name__=="__main__":
	r=Router("R1")
	print r