import Queue
import logger
import clock
class PacketTracker:
	def __init__(self):
		self.expect=0
		self.exist=Queue.PriorityQueue()
		self.ini=0
	def handler(self,packet):
		#logger.table.flow_rate_log(packet.flow_id, (self.ini+self.expect+self.exist.qsize())*1024/clock.clk.get_time(), clock.clk.get_time())
		logger.table.flow_rate_log(packet.flow_id, 1, clock.clk.get_time())
		
		if packet.id==self.expect:
			self.expect=self.expect+1
			while(not self.exist.empty() and self.expect==self.exist.queue[0]):
				self.expect=self.expect+1
				self.exist.get()
		elif packet.id>self.expect:
			if(not packet.id in self.exist.queue):
				self.exist.put(packet.id)
			else:
				self.ini+=1 
		else:
			return
	
	