class Link:
	def __init__(self,linkObject):
		self.id=linkObject['id']
		self.rate=linkObject['rate']
		self.delay=linkObject['delay']
		self.buffer=linkObject['buffer']
		self.endpoints=linkObject['endpoints']