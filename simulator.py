from link import Link
from router import Router
from host import Host
from flow import Flow
import json

class Simulator:
	def __init__(self):
		self.jsonObject=self.readData()
		self.link=Link(self.jsonObject['links'][0])
		self.host=Host(self.jsonObject['hosts'][0])
		#self.router=Router(self.jsonObject['routers'][0])
		self.flow=Flow(self.jsonObject['flows'][0])
		self.clock=0
		
	def readData(self):
		return json.load(file('testcase0.json'))  
	def run(self):
		return

if __name__=="__main__":
	simulator=Simulator();
		