class Packet:
	def __init__(self,packetObject):
		self.id=packetObject['id']
		self.source=packetObject['source']
		self.destination=flowObject['destination']
		self.amount=flowObject['amount']
		self.size=