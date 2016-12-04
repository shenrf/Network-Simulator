import sys
from event import FlowWakeEvent
import clock
import logger
#from flow import Flow
#from event_queue import event_scheduler
slow_start = "Slow Start"
congestion_avoidance = "Congestion Avoidance"
fast_recovery = "Fast Recovery"
class CongestionControllerFast():
	def __init__(self,flow):
		self.cwnd = 2.0
		#logger.table.window_log(flow.id, self.cwnd, clock.clk.get_time())
		self.timeout = 1
		self.no_ack = dict() #packet id, packet sent timespam
		self.timed_out = [] #list of packet
		self.dup_count = 0
		self.last_ack_received = -1 #packet id
		self.window_start = 0 # id for the first packet in window
		self.retransmit = False
		self.flow = None
		self.wake_event = None
		self.event_scheduler = None
		clock = None
		self.event_scheduler=None
		self.alpha = 30.0
		self.flow=flow
		self.gama = 0.02
		self.base_RTT = -1
	#handle an ack packet and update window size
	def ack_received(self, packet):
		print "receive"
		if self.wake_event != None:
			self.event_scheduler.cancel_event(self.wake_event)
		# Check if this is a duplicate ack
		if packet.next_id == self.last_ack_received:
			self.dup_count += 1
			keys= [key for key in self.no_ack.keys() if key[0] == packet.next_id]
			# 3 duplicate ack and packet has not been received, re-send
			if (self.dup_count == 3) and (len(keys) > 0):
				expected = keys[0]
				del self.no_ack[(packet.next_id, expected[1])]
				self.timed_out.append((packet.next_id,expected[1]))
		# not a duplicate ack
		else:
			self.dup_count = 0
		self.last_ack_received = packet.next_id
		# ack for unacknowlefged packet
		if (packet.id, packet.duplicate_num) in self.no_ack.keys():
			#print "waiting input"
			#a=input()
			#calculate RTT
			rtt = clock.clk.get_time() - self.no_ack[(packet.id, packet.duplicate_num)]
			logger.table.packet_delay_log(self.flow.id, rtt, clock.clk.get_time())
			# the first calculated rtt
			if self.base_RTT == -1:
				self.base_RTT = rtt
			# update window size
			print self.cwnd
			self.cwnd = min(2 * self.cwnd, (1 - self.gama) * self.cwnd + self.gama * (self.cwnd * self.base_RTT / rtt + self.alpha))
			print "update cwnd ackreceive update cwnd ackreceive"
			print rtt
			print self.base_RTT
			print self.cwnd
			print "update cwnd ackreceive update cwnd ackreceive"
			logger.table.window_log(self.flow.id, self.cwnd, clock.clk.get_time())
			# update minimum RTT
			if rtt < self.base_RTT:
				self.base_RTT = rtt
			del self.no_ack[(packet.id, packet.duplicate_num)]
				
		# check for timed out packet
		for (packet_id, dup_num) in self.no_ack.keys():
			sent_time = self.no_ack[(packet_id, dup_num)]
			time_diff =  clock.clk.get_time() - sent_time
			if time_diff > self.timeout:
				del self.no_ack[(packet_id, dup_num)]
				self.timed_out.append((packet_id, dup_num))
		if len(self.timed_out) > 0:
			print len(self.timed_out)
			a = input("check timed out packet ack_receive")
			self.retransmit = True
			self.cwnd /= 2
			print "cwnd/2 ackreceive cwnd/2 ackreceive cwnd/2 ackreceive"
			print self.cwnd
			print "cwnd/2 ackreceive cwnd/2 ackreceive cwnd/2 ackreceive"
			logger.table.window_log(self.flow.id, self.cwnd, clock.clk.get_time())
		else:
			self.retransmit = False

		flag=self.send_packet()
		if(flag==True):
			self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))
		#print "here:"+str(self.cwnd)
		#print self.event_scheduler
	#send packets in the window size
	def send_packet(self):
		#a = input("insend_packet")
		#print "there"
		if self.retransmit == True:
		#send timed out packets
			print len(self.no_ack)
			print self.cwnd
			print len(self.timed_out)
			a = input("check timed out packet send_packet")
			#a = input("outwhile")
			while (len(self.timed_out) < self.cwnd) and (len(self.timed_out) > 0):
				#print packet_id
				#a=input("inwhile ")
				flag = True
				(packet_id, dup_num) = self.timed_out[0]
				self.no_ack[(packet_id, dup_num + 1)] = clock.clk.get_time()
				# flow send a packet
				self.flow.send_data_packet(packet_id, dup_num + 1)
				del self.timed_out[0]
			
		else:
		# send new packets
			flag=False
			while (len(self.no_ack) < self.cwnd) and (self.window_start * 1024 < self.flow.total_amount):
				# flow send a packet
				flag=True
				self.no_ack[(self.window_start, 0)] = clock.clk.get_time()
				self.flow.send_data_packet(self.window_start,0)
				self.window_start += 1
			return flag
	#start sending packet when congestion control first begin or the flow time out
	def wake(self):
		#unacknowledged packets that time out
		for packet_id in self.no_ack.keys():
			sent_time = self.no_ack[packet_id]
			time_diff = clock.clk.get_time() - sent_time
			if time_diff > self.timeout:
				del self.no_ack[packet_id]
				self.timed_out.append(packet_id)
			# there are timed out packets
			if len(self.timed_out) > 0:
				self.retransmit = True
			else:
				self.retransmit = False
        ############################################
		# self.cwnd /= 2
		#print "cwnd/2 wake cwnd/2 wake cwnd/2 wake"
		#print self.cwnd
		#print "cwnd/2 wake cwnd/2 wake cwnd/2 wake"
		#logger.table.window_log(self.flow.id, self.cwnd, clock.clk.get_time())
		flag=self.send_packet()
		if(flag==True):
			self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))
		#print "end of wake function: "+ str(self.cwnd)

class CongestionControllerReno():
	def __init__(self,flow):
		self.cwnd = 1.0
		self.timeout = 1
		self.no_ack = dict() #packet id, packet sent timespam
		self.time_out = [] #list of packet
		self.dup_count = 0
		self.last_ack_received = -1 #packet id
		self.window_start = 0 # id for the first packet in window
		self.retransmit = False
		self.flow = None
		self.wake_event = None
		self.event_scheduler = None
		clock = None
		self.ssthresh = None
		self.state = slow_start
		self.FR_packet = None
		self.flow=flow
		self.keys = []
	# process the ack
	def ack_received(self, packet):
		# check for timed-out unacknowledge packets
		print str(self.state)

		for (packet_id, dup_num) in self.no_ack.keys():
			send_time = self.no_ack[(packet_id, dup_num)]
			time_diff = clock.clk.get_time() - send_time 	# need current time!!!!
			if time_diff > self.timeout and self.state != fast_recovery:
				del self.no_ack[(packet_id, dup_num)]
				self.time_out.append((packet_id, dup_num))

		# setup for retransmission	
		if len(self.time_out) > 0:
			#a = input()
			self.ssthresh = self.cwnd/2
			#self.cwnd = 1
			#self.state = slow_start
			#self.no_ack = dict()
			self.retransmit = True
		else:
			self.retransmit = False
		

		#if len(self.time_out) == 0:
			#self.retransmit = False;

		if self.wake_event != None:
			self.event_scheduler.cancel_event(self.wake_event)

		# delete acknowledged packet
		if (packet.id, packet.duplicate_num) in self.no_ack.keys():
			rtt = clock.clk.get_time() - self.no_ack[(packet.id, packet.duplicate_num)]
			logger.table.packet_delay_log(self.flow.id, rtt, clock.clk.get_time())
			print "delete no_ack" + str(packet.id) + str(packet.duplicate_num)
			del self.no_ack[(packet.id, packet.duplicate_num)]
			#if (packet.duplicate_num == 1):
				#a = input("del pack dup = 1")
			

		if self.state == slow_start and self.retransmit == False:
			self.cwnd += 1
			if self.ssthresh != None and self.cwnd >= self.ssthresh:
				self.state = congestion_avoidance
		elif self.state == congestion_avoidance and self.retransmit == False:
			if packet.next_id == self.last_received_ack:
				self.dup_count += 1
				if (self.dup_count == 3) and (packet.next_id in [key[0] for key in self.no_ack.keys()]):
					self.cwnd /= 2
					self.ssthresh = self.cwnd
					self.cwnd += 3
					self.state = fast_recovery
			else:
				self.cwnd += 1 / self.cwnd
				self.dup_count = 0
		elif self.state == fast_recovery:
			#a = input()
			print "FR"
			self.cwnd += 1
			if packet.next_id == self.last_received_ack:
				self.dup_count += 1
				self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))
				return
			else:
				if packet.id == self.FR_packet:
					self.cwnd = self.ssthresh
					self.state = congestion_avoidance
				self.dup_count = 0
		self.last_received_ack = packet.next_id
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print self.cwnd
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		logger.table.window_log(self.flow.id, self.cwnd, clock.clk.get_time())
		flag=self.send_packet()
		
		self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))


	def send_packet(self):
		if self.state == slow_start or self.state == congestion_avoidance:
			flag = False
			if self.retransmit == True:	
				print "retransmit!" + str(self.time_out[0])
				#a = input()
				print str(self.time_out)
				print "cwnd " + str(self.cwnd) + " no_ack " +str(len(self.no_ack))+ str(len(self.no_ack) < self.cwnd)
				while (len(self.no_ack) < self.cwnd) and (len(self.time_out) > 0):
					flag = True
					(packet_id, dup_num) = self.time_out[0]
					self.no_ack[(packet_id, dup_num + 1)] = clock.clk.get_time()		# clock!!!
					self.flow.send_data_packet(packet_id, dup_num + 1)	# flow.send!!!!
					del self.time_out[0]
					print "del " + str(packet_id) +" "+ str(dup_num)
					#a = input()
				self.retransmit == False
			else:
				#send new packets
				print "cwnd " + str(self.cwnd) + " no_ack " +str(len(self.no_ack))
				print "no_ack < cwnd?" + str(len(self.no_ack) < self.cwnd) 
				print "window_start < total?" + str(self.window_start * 1024 < self.flow.total_amount)
				while (len(self.no_ack) < self.cwnd) and (self.window_start * 1024 < self.flow.total_amount):
					flag = True
					self.no_ack[(self.window_start, 0)] = clock.clk.get_time()
					self.flow.send_data_packet(self.window_start, 0)
					self.window_start += 1
					print "window_start " + str(self.window_start)
		else:
			flag = False
			packet_id = self.last_received_ack
			self.FR_packet = packet_id
			for key in self.no_ack.keys():
				if key[0] == packet_id:
					self.keys.append(key)
			print "len(self.keys) " + str(len(self.keys))
			if len(self.keys) == 1:
				print "len(self.keys) == 1"
				dup_num = self.keys[0][1]
				del self.no_ack[self.keys[0]]
				self.no_ack[(packet_id, dup_num + 1)] = clock.clk.get_time()
				self.flow.send_data_packet(packet_id, dup_num + 1)
				flag=True
			self.keys = []
		return flag

	def wake(self):
		if self.state == fast_recovery:
			self.state = slow_start
		else:
			self.cwnd/= 2

		for (packet_id, dup_num) in self.no_ack.keys():
			send_time = self.no_ack[(packet_id, dup_num)]
			time_diff = clock.clk.get_time() - send_time
			if time_diff > self.timeout:
				del self.no_ack[(packet_id, dup_num)]
				self.time_out.append((packet_id, dup_num))
		if len(self.time_out) > 0:
			self.ssthresh = self.cwnd/2
			#self.state = slow_start
			#self.cwnd = 1
			#self.no_ack = dict()
			self.retransmit = True
		else:
			self.retransmit = False  
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print self.cwnd
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"
		print "ajdksfjladksfjlkdsajklfjlkdsajfjlkkjlfdsalkjf33333333333333333333"	 
		logger.table.window_log(self.flow.id, self.cwnd, clock.clk.get_time())
		flag=self.send_packet()
		if(flag==True):
			self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))  
		#print "cwnd: ", str(self.cwnd)
		
	def __str__(self):
		return ("ssthresh:       " + str(self.ssthresh) + "\n"
				"cwnd:           " + str(self.cwnd) + "\n"
				"duplicate ACKS: " + str(self.dup_count) + "\n")    