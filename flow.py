class Flow:
	def __init__(self,flowObject):
		self.id=flowObject['id']
		self.source=flowObject['source']
		self.destination=flowObject['destination']
		self.amount=flowObject['amount']
		self.start=flowObject['start']