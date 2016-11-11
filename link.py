import Queue,random,json
from event import LinkReadyEvent, PacketArrivalEvent

class Buffer:
	def __init__(self,capacity):
		self.capacity=capacity
		self.buffer=Queue.Queue(self.capacity)
	def available(self):
		return self.capacity-self.size()
	def size(self):
		return self.buffer.qsize()
	def get(self):
		return self.buffer.get()
	def isEmpty(self):
		return self.buffer.empty()
	def put(self,packet,destination):
		if(packet.size<=self.available()):
			self.buffer.put((packet,destination))
			return True
		else:
			return True

class Link:
	def __init__(self,linkObject):
		self.id=linkObject['id']
		self.rate=linkObject['rate']
		self.delay=linkObject['delay']
		self.buffer_size=linkObject['buffer']
		self.pointA=None
		self.pointB=None
		self.buffer=Buffer(self.buffer_size)
		self.busy=False
		self.scheduler=None
	def __str__(self):
		return "Link id:"+str(self.id)+" rate:"+str(self.rate)+" dealy:"+str(self.delay) \
			+" buffer:"+str(self.buffer_size)
	def send(self,packet,sender):
		if(sender==self.pointA):
			receiver=self.pointB
		else:
			receiver=self.pointA
	#if link is busy, put into buffer,else send the packet
		if(self.busy):
			self.buffer.put(packet,receiver)
		else:
			self.busy=True
			delay=self.delay+packet.size/self.rate;
			self.scheduler.put_event(delay,PacketArrivalEvent(packet,receiver,self))
			self.scheduler.put_event(self.delay,LinkReadyEvent(self))
	def wakeup(self):
		self.busy=False
		if(not self.buffer.isEmpty()):
			(packet,destination)=self.buffer.get()
			send(packet,destination)



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