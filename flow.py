class Flow:
	"""  
	    -id is the identifier of the flow object;
	    -source would be node that send outs the packets;
	    -destination would be the destination of each packets;
	    -amount would be the data amount in bytes that we send the packets;
	    -start is the start time of the flow process
	
	"""
	def __init__(self,flowObject):
		self.id=flowObject['id']
		self.source=flowObject['source']
		self.destination=flowObject['destination']
		self.amount=flowObject['amount']
		self.start=flowObject['start']
	def runTime(self):
		return str(self.start)

class Packet:
	def __init__(self,size):
		self.size=size
		
