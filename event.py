#import math
class Event:
	def __init__(self,priority,flow):
		self.priority=priority
		self.flow=flow
	def __cmp__(self,other):
		return cmp(self.priority,other.priority)