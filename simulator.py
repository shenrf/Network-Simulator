from link import Link
from router import Router
from host import Host
from flow import Flow
from event import Event
import json
import Queue
class Simulator:
	def __init__(self):
		jsonObject=self.readData()
		# initialize the hosts,flows,routers,links
		self.links={};
		for l in jsonObject['links']:
			self.links[l['id']]=Link(l)
		self.hosts={}
		for h in jsonObject['hosts']:
			self.hosts[h['id']]=Host(h)
		self.flows={}
		for f in jsonObject['flows']:
			self.flows[f['id']]=Flow(f)
		self.routers={}
		for r in jsonObject['routers']:
			self.routers[r['id']]=Router(r)
			
		self.queue=Queue.PriorityQueue()
		for f in self.flows:
			self.queue.put(Event(self.flows[f].runTime(),f))
		
		self.clock=0
		
	def readData(self):
		return json.load(file('testcase1.json'))  
	def run(self):
		return

if __name__=="__main__":
	simulator=Simulator();
		