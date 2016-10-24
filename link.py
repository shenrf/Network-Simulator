class Link:
	def __init__(self,linkObject):
		self.id=linkObject['id']
		self.rate=linkObject['rate']
		self.delay=linkObject['delay']
		self.buffer=linkObject['buffer']
		self.endpoints=linkObject['endpoints']
	def __str__(self):
		return "Link id:"+str(self.id)+" rate:"+str(self.rate)+" dealy:"+str(self.delay)

class Buffer:
	def __init__(self,capacity):
		self.capacity=capacity
		self.busy=False
		self.use=0
