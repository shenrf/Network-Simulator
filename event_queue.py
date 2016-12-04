import Queue
from event import Event,FlowWakeEvent,LinkReadyEvent,PacketArrivalEvent,RoutingUpdateEvent
#from flow import Router_Packet
import clock
import logger
class EventQueue:
	def __init__(self,time):
		self.current_time=time
		self.queue=Queue.PriorityQueue()
		self.rout=None
	def blind(self,router):
		self.rout=router
	def __str__(self):
		res=""
		return str(self.queue)
	def put_event(self,delay,e):
		self.queue.put((self.current_time+delay,e))
		return e
	def add_event(self,time,e):
		self.queue.put(time,e)
	def pop_event(self):
		(t,e)=self.queue.get()
		return t,e
	def get_event(self):
		while(not self.queue.empty()):
			(new_time,e)=self.queue.get()
			#print float(new_time)
			self.current_time=new_time
			clock.clk.update_time(new_time)
			print new_time
			
			self.current_time=new_time
			#if(isinstance(e,RoutingUpdateEvent)):
				#for id in self.rout:
				#	print self.rout[id]
				#print "warint input:"
				#a=input()

			if(isinstance(e,PacketArrivalEvent)):
				'''
				if(~isinstance(e.packet,Router_Packet)):
					e.from_link.log.addx(new_time)
					e.from_link.log.addy(e.from_link.rate)
					e.from_link.log.addx(new_time+0.001)
					e.from_link.log.addy(0)
				'''
				logger.table.clock_log(new_time)
				logger.table.link_rate_log(e.from_link.id, e.from_link.rate, new_time)
				#logger.table.buff_occupancy_log(e.from_link.id, e.from_link.buffer.size(), new_time)
			return e
		return None
	def cancel_event(self,e):
		#print "cancel: "
		e.canceled=True
	def isEmpty(self):
		return self.queue.empty()