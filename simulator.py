from link import Link
from router import Router
from host import Host
from flow import Flow
from event import Event,FlowWakeEvent,LinkReadyEvent,PacketArrivalEvent
from event_queue import EventQueue
from device import Device,Host
import json
import Queue

class Simulator:
	def __init__(self):
		jsonObject=self.readData()
		# initialize the hosts,flows,routers,links
		self.queue=EventQueue(0)
		self.hosts={}
		for h in jsonObject['hosts']:
			self.hosts[h['id']]=Host(h['id'])
		self.links={};
		for l in jsonObject['links']:
			self.links[l['id']]=Link(l)
			self.links[l['id']].scheduler=self.queue
			self.links[l['id']].pointA=self.hosts[l['endpoints'][0]]
			self.links[l['id']].pointB=self.hosts[l['endpoints'][1]]
			self.hosts[l['endpoints'][0]].link=self.links[l['id']]
			self.hosts[l['endpoints'][1]].link=self.links[l['id']]
		self.flows={}
		for f in jsonObject['flows']:
			self.flows[f['id']]=Flow(f)
			self.flows[f['id']].source=self.hosts[f['source']]
			self.hosts[f['source']].flow[f['id']]=self.flows[f['id']]
			self.flows[f['id']].destination=self.hosts[f['destination']]
			self.hosts[f['destination']].flow[f['id']]=self.flows[f['id']]
		self.routers={}
		for r in jsonObject['routers']:
			self.routers[r['id']]=Router(r)
		for id in self.flows:
			self.queue.put_event(self.flows[id].start_time,FlowWakeEvent(self.flows[id]))
		self.clock=0
	def readData(self):
		return json.load(file('testcase0.json'))  
	def run(self):
		while(not self.queue.isEmpty()):
			e=self.queue.get_event()
			e.perform()

if __name__=="__main__":
	simulator=Simulator()
	simulator.run()
	print simulator.queue.current_time