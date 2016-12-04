import Queue,random,json
from event import LinkReadyEvent, PacketArrivalEvent
from flow import Router_Packet, Data_Packet
import logger
class Buffer:
	'''
	self.capacity: the size of the buffer
	self.buffer: the FIFO queue
	'''
	def __init__(self,capacity):
		self.capacity=capacity
		self.buffer=Queue.Queue(self.capacity)
		self.link=None
		self.used=0.0
	def available(self):
		return self.capacity-self.used
	def size(self):
		return self.used/self.capacity
	def get(self):
		(p,d)= self.buffer.get()
		self.used=self.used-p.size
		return p,d
	def isEmpty(self):
		return self.buffer.empty()
	def put(self,packet,destination):
		#logger.table.buff_occupancy_log(self.link.id,self.used/self.capacity,self.link.scheduler.current_time)
		if(packet.size<=self.available()):
			self.buffer.put((packet,destination))
			self.used=self.used+packet.size
			return True
		else:
			if(isinstance(packet,Data_Packet)):
				logger.table.packet_packet_loss_log(self.link.id,1,self.link.scheduler.current_time)
			return True
	''' 
		self.id: the id number of the link
		self.rate: the transfer rate of the link
		self.delay: the delay time cost of the link
		self.busy: judge whether the link is busy right now
		self.scheduler: referenced to the event_queue in the simulator
		self.pointA: one of the endpoints, might be a host or a router
		self.pointB: one of the endpoints, might be a host or a router
		self.buffer_size: record the size of the buffer
	'''
class Link:
	def __init__(self,linkObject):
		self.id=linkObject['id']
		self.rate=float(linkObject['rate'])
		self.delay=float(linkObject['delay'])
		self.buffer_size=linkObject['buffer']
		self.pointA=None
		self.pointB=None
		self.buffer=Buffer(self.buffer_size)
		self.buffer.link=self
		self.busy=False
		self.scheduler=None
		self.direction=False
		self.pre_receive=None
	def __str__(self):
		#return "Link id:"+str(self.id)+" rate:"+str(self.rate)+" delay:"+str(self.delay) \
		#	+" buffer:"+str(self.buffer_size)+" endpoints"+ str(self.pointA)+" "+str(self.pointB)
		return str(self.id)
	def get_occupancy(self):
		return self.buffer.used
	def send(self,packet,sender):
		logger.table.buff_occupancy_log(self.id,self.buffer.used/self.buffer.capacity,self.scheduler.current_time)
		if(sender==self.pointA):
			receiver=self.pointB
		else:
			receiver=self.pointA
	#if link is busy, put into buffer,else send the packet
		if(self.busy):
			self.buffer.put(packet,sender)
			#print "busy"
			#a=input()
		else:
			self.busy=True
			delay=packet.size/self.rate
			cur_time=self.scheduler.current_time
			'''if(~ isinstance(packet,Router_Packet)):
				self.log.addx(cur_time)
				self.log.addy(0)
				self.log.addx(cur_time+0.0001)
				self.log.addy(self.rate)
			'''
            #print delay+self.delay+cur_time
            #print "here"
            #print str(self.rate)+" "+str(self.delay)+" "+str(packet.size)
			if(self.pre_receive== None or receiver!=self.pre_receive):
				self.pre_receive=receiver
				self.scheduler.put_event(round(delay+self.delay,4),PacketArrivalEvent(packet,receiver,self))
				self.scheduler.put_event(round(delay,4),LinkReadyEvent(self))
			else:
				self.scheduler.put_event(round(delay+self.delay,4),PacketArrivalEvent(packet,receiver,self))
				self.scheduler.put_event(round(delay,4),LinkReadyEvent(self))

	def init_router(self):
		packet1=Router_Packet(self.delay,self.pointA,self,0,0)
		packet2=Router_Packet(self.delay,self.pointB,self,0,0)
		self.scheduler.put_event(self.delay,PacketArrivalEvent(packet1,self.pointB,self))
		self.scheduler.put_event(0,LinkReadyEvent(self))
		self.scheduler.put_event(self.delay,PacketArrivalEvent(packet2,self.pointA,self))
		self.scheduler.put_event(0,LinkReadyEvent(self))
	def wakeup(self):
		self.busy=False
		if(not self.buffer.isEmpty()):
			(packet,destination)=self.buffer.get()
			self.send(packet,destination)


if __name__=="__main__":
	jsonObject=json.load(file('testcase1.json'))
	links={};
	for l in jsonObject['links']:
		links[l['id']]=Link(l)
	l1=links.get('L1')
	'''link_temp=links.get('L1')
	for i in range(10):
		rand=random.randint(1,99)
		link_temp.buffer.put("hello")
		print link_temp.buffer.size()
	while(not link_temp.buffer.isEmpty()):
		print link_temp.buffer.get()'''