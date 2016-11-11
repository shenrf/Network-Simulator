import Queue
from event import Event,FlowWakeEvent,LinkReadyEvent,PacketArrivalEvent
class EventQueue:
	def __init__(self,time):
		self.current_time=time
		self.queue=Queue.PriorityQueue()
	def put_event(self,delay,e):
		self.queue.put((self.current_time+delay,e))
	def get_event(self):
		while(not self.queue.empty()):
			(new_time,e)=self.queue.get()
			self.current_time=new_time
			return e
		return None
	def isEmpty(self):
		return self.queue.empty()