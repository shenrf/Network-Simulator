from link import Link
#from router import Router
from flow import Flow
from event import Event,FlowWakeEvent,LinkReadyEvent,PacketArrivalEvent, RoutingUpdateEvent
from event_queue import EventQueue
from device import Device,Host,Router
import json
import Queue
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from fasttcp import CongestionControllerFast,CongestionControllerReno
from packet_tracker import PacketTracker
import clock
import graph
import logger
import csv

case=2
class Simulator:
	def __init__(self):
		jsonObject=self.readData()
		# initialize the hosts,flows,routers,links
		self.queue=EventQueue(0)
		self.routers={}
		for r in jsonObject['routers']:
			self.routers[r['id']]=Router(r['id'])
		self.hosts={}
		for h in jsonObject['hosts']:
			self.hosts[h['id']]=Host(h['id'])
		self.links={}
		for l in jsonObject['links']:
			self.links[l['id']]=Link(l)
			self.links[l['id']].scheduler=self.queue
			if(l['endpoints'][0][0]=='H' or l['endpoints'][0][0]=='S' or l['endpoints'][0][0]=='T'):
				self.links[l['id']].pointA=self.hosts[l['endpoints'][0]]
				self.hosts[l['endpoints'][0]].link=self.links[l['id']]
			else:
				self.links[l['id']].pointA=self.routers[l['endpoints'][0]]
				self.routers[l['endpoints'][0]].links.append(self.links[l['id']])
			if(l['endpoints'][1][0]=='H' or l['endpoints'][1][0]=='S' or l['endpoints'][1][0]=='T'):
				self.links[l['id']].pointB=self.hosts[l['endpoints'][1]]
				self.hosts[l['endpoints'][1]].link=self.links[l['id']]
			else:
				self.links[l['id']].pointB=self.routers[l['endpoints'][1]]
				self.routers[l['endpoints'][1]].links.append(self.links[l['id']])
		self.flows={}
		for f in jsonObject['flows']:
			self.flows[f['id']]=Flow(f)
			self.flows[f['id']].event_queue=self.queue
			self.flows[f['id']].controller.event_scheduler=self.queue
			self.flows[f['id']].source=self.hosts[f['source']]
			self.hosts[f['source']].flow[f['id']]=self.flows[f['id']]
			self.flows[f['id']].destination=self.hosts[f['destination']]
			self.hosts[f['destination']].flow[f['id']]=self.flows[f['id']]
		self.queue.blind(self.routers)
	def readData(self):
		if case==1:
			return json.load(file('testcase1.json'))
		if case==2:
			return json.load(file('testcase2.json'))
	def run(self):
		self.queue.current_time=0
		for id in self.flows:
			self.queue.put_event(self.flows[id].start_time,FlowWakeEvent(self.flows[id]))
		for id in self.hosts:
			self.queue.put_event(5,RoutingUpdateEvent(self.hosts[id]))
		while(not self.queue.isEmpty()):
			e=self.queue.get_event()
			if(e.canceled==False):
				#print e
				#print clock.clk.get_time()
				#a=input()
				e.perform()
	def init_router_table(self):
		for id in self.links:
			self.links[id].init_router()
		while(not self.queue.isEmpty()):
			e=self.queue.get_event()
			if(e.canceled==False):
				#print e
				e.perform()

if __name__=="__main__":
	simulator=Simulator()
	simulator.init_router_table()
	#print "routing table initiated: "
	#print simulator.queue.current_time
	#for id in simulator.routers:
	#	print simulator.routers[id]
	'''print "start"
	simulator.queue.put_event(0,"here")
	print simulator.queue
	simulator.queue.put_event(1,"here")
	print simulator.queue
	simulator.queue.cancel_event("here")
	#simulator.run()
	print simulator.queue.current_time'''
	simulator.run()
    #print logger.table.table_packet_loss
    #print logger.table.clock_packet_loss
	#graph.g.packet_packet_loss_graph(1,'hi')
	print clock.clk.get_time()
	for f in simulator.flows:
		print simulator.flows[f].controller.window_start * 1024
		print simulator.flows[f].total_amount
	
	print clock.clk.get_time()
	print clock.clk.get_time()
	print clock.clk.get_time()
	print clock.clk.get_time()

	graph.g.link_rate_graph(case,'Link Rate (Mbps)')
	graph.g.buff_occupancy_graph(case,'Buffer Occupancy (pkts)')
	graph.g.window_size_graph(case,'Window Size (pkts)')
	graph.g.flow_rate_graph(case,'Flow Rate (Mbps)')
	graph.g.packet_loss_graph(case,'Packet Loss (pkts)')
	graph.g.packet_delay_graph(case,'Packet Delay (second)')
	#print "adfasdfasd"
	#print "adfasdfasd"
	#print "adfasdfasd"
	#print "adfasdfasd"
	#print "adfasdfasd"
	#print "adfasdfasd"
	#print logger.table.clock_window
	#print logger.table.table_window
	#print 
	#print 
	#for key in logger.table.table_window:
            #print key
	
	'''
	f=open('data.txt','w')
	f.write('window size  \n')
	f.write('F1' + '\n')
	f.write(logger.table.table_window['F1']+ '\n')
	f.write(logger.table.clock_window['F1']+ '\n')
	#a=input("1")

	f.write('L1 \n')
	f.write(logger.table.table_packet_loss['L1']+ '\n')
	f.write(logger.table.clock_packet_loss['L1']+ '\n')
	f.write('L2 \n')
	f.write(logger.table.table_packet_loss['L2']+ '\n')
	f.write(logger.table.clock_packet_loss['L2']+ '\n')
	'''
	'''
	f.write('window size  \n')

	f.write('L1' + '\n')
	f.write(logger.table.table_window['L1']+ '\n')
	f.write(logger.table.clock_window['L1']+ '\n')
	'''
	'''
	f.write('packet delay  \n')
	for key in logger.table.table_packet_delay:
		f.write(key + '\n')
		f.write(logger.table.table_packet_delay[key]+ '\n')
		f.write(logger.table.clock_packet_delay[key]+ '\n')

	f.write('flow rate  \n')
	for key in logger.table.table_flow_rate:
		f.write(key + '\n')
		f.write(logger.table.table_flow_rate[key]+ '\n')
		f.write(logger.table.clock_flow_rate[key]+ '\n')

	f.write('packet loss  \n')
	for key in logger.table.table_packet_loss:
		f.write(key + '\n')
		f.write(logger.table.table_packet_loss[key]+ '\n')
		f.write(logger.table.clock_packet_loss[key]+ '\n')
	'''
	#f.close()
	
	#w = csv.writer(open("output.csv", "w"))
	#for key, val in logger.table.table_window.items():
		#w.writerow([key, val])
