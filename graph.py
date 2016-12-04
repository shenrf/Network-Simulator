import matplotlib.pyplot as plt
from scipy import signal
import random
import logger
import clock
import numpy as np
from numpy.random import randn
from numpy.fft import rfft
from scipy import signal
import simulator
"""
	title = 'Case ' + str(case) + ' ' + category
	figure, axes = plt.subplots()
	figure.canvas.set_window_title(title)
	axes.set_title(title)
	axes.set_xlabel('Time (s)')
	units = 'Mbps' if category == 'Flow Rate' else 'packets / second'
	axes.set_ylabel(category + ' (' + units + ')')
	record_name = '_'.join(category.lower().split(' '))
	axes.legend()
"""

class Graph:
	def link_rate_graph(self, case, descriptor):
		b1, a1 = signal.butter(2, 0.03)
		figure, axes=plt.subplots()
		title='Link Rate:  Case ' + str(case) 
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#now printing out the dictionary as plot
		num=0
		#print sorted(list(set(logger.table.table_clock)))
		for key in logger.table.table_link_rate:
			if simulator.case==2:
				if (key == 'L2') or (key == 'L1') or (key == 'L3'):
					print key 
					x=logger.table.clock_link_rate[key]
					x.insert(0,0)
					y=logger.table.table_link_rate[key]
					y.insert(0,0)
					#print x
					#print y
					i=0
					#num=0
				
					y=[y *8 / 10**6 for y in y]
					a=[]
					b=[]
					while i< len(x):
						temp=x[i]
						sum=1
						while i < len(x)-1:
							if (x[i+1]-temp<0.011):
								i=i+1
								sum=sum+1
							else:
								break
						if (i==len(x)):
							i=i-1
						a.append(x[i])
						b.append(sum*1024)
						i=i+1
					'''
					i=1
					while i<len(b):
						if (a[i]-a[i-1]>1):
							b.insert(i,0)
							a.insert(i,a[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							b.insert(i,0)
							a.insert(i,a[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					'''
					#if (key == 'L2'):
					#    y=[y *1.0 for y in y]
					#plt.ylim(0, 3)
					#b=signal.lfilter(b1, a1, signal.lfilter(b1, a1, b))
					i=1
					while i<len(b):
						if (a[i]-a[i-1]>1):
							b.insert(i,0)
							a.insert(i,a[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							b.insert(i,0)
							a.insert(i,a[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					b=signal.lfilter(b1, a1, signal.lfilter(b1, a1, b))
					b=[b / 6000 *2.5 for b in b]
					if (key == 'L2'):
						plt.plot(a,b,'r',label=key)
					if (key == 'L1'):
						plt.plot(a,b,'k',label=key)
					if (key == 'L3'):
						plt.plot(a,b,'g',label=key)
			else:
				if (key == 'L2') or (key == 'L1'):
					print key 
					x=logger.table.clock_link_rate[key]
					x.insert(0,0)
					y=logger.table.table_link_rate[key]
					y.insert(0,0)
					#print x
					#print y
					i=0
					#num=0
				
					y=[y *8 / 10**6 for y in y]
					a=[]
					b=[]
					while i< len(x):
						temp=x[i]
						sum=1
						while i < len(x)-1:
							if (x[i+1]-temp<0.111):
								i=i+1
								sum=sum+1
							else:
								break
						if (i==len(x)):
							i=i-1
						a.append(x[i])
						b.append(sum*1024)
						i=i+1
					
					i=1
					while i<len(b):
						if (a[i]-a[i-1]>1):
							b.insert(i,0)
							a.insert(i,a[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							b.insert(i,0)
							a.insert(i,a[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					
					b=signal.lfilter(b1, a1, signal.lfilter(b1, a1, b))
					b=[b / 6000 *2.5 for b in b]
					if (key == 'L2'):
						plt.plot(a,b,'*',label=key)
					else:
						plt.plot(a,b,'x',label=key)
			
		#And do the plotting
		axes.legend()
		plt.show()
		

	def buff_occupancy_graph(self, case, descriptor):
		b, a = signal.butter(2, 0.03)
		#b, a = signal.butter(2, 0.08)
		figure, axes=plt.subplots()
		title='Buffer Occupancy:  Case ' + str(case)
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#b, a = signal.butter(2, 0.03, analog=False)
		#now printing out the dictionary as plot
		for key in logger.table.table_buff_occupancy:
			#print logger.table.table_buff_occupancy[key]
			#print "buffer "+ key + " "
			#print logger.table.table_buff_occupancy[key]
			if simulator.case == 2:
				if (key == 'L2') or (key == 'L1') or (key == 'L3'):
					x=logger.table.clock_buff_occupancy[key]
					y=logger.table.table_buff_occupancy[key]
					#y = signal.lfilter(b, a, signal.lfilter(b, a, y))
					i=1
					while i<len(y):
						if (x[i]-x[i-1]>1):
							y.insert(i,0)
							x.insert(i,x[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							y.insert(i,0)
							x.insert(i,x[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					y2 = signal.lfilter(b, a, signal.lfilter(b, a, y))
					y3 = signal.lfilter(b, a, signal.lfilter(b, a, y))
					plt.plot(x,y3,label=key)
			else:
				if (key == 'L2') or (key == 'L1'):
					x=logger.table.clock_buff_occupancy[key]
					y=logger.table.table_buff_occupancy[key]
					i=1
					while i<len(y):
						if (x[i]-x[i-1]>1):
							y.insert(i,0)
							x.insert(i,x[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							y.insert(i,0)
							x.insert(i,x[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					#y2 = signal.lfilter(b, a, signal.lfilter(b, a, y))
					plt.plot(logger.table.clock_buff_occupancy[key],logger.table.table_buff_occupancy[key],label=key)
			#And do the plotting
		#axes.legend()
		axes.legend()
		plt.show()

		
	def flow_rate_graph(self, case, descriptor):
		b1, a1 = signal.butter(2, 0.03)
		figure, axes=plt.subplots()
		title='Flow rate:  Case ' + str(case) 
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#now printing out the dictionary as plot
		for key in logger.table.table_flow_rate:
			#print logger.table.table_flow_rate[key]
			'''
			x=logger.table.clock_flow_rate[key]
			y=logger.table.table_flow_rate[key]
			y=[y *8 / 10**6 for y in y]
			'''
			print key 
			x=logger.table.clock_flow_rate[key]
			x.insert(0,0)
			y=logger.table.table_flow_rate[key]
			y.insert(0,0)
					#print x
					#print y
			i=0
					#num=0
				
			y=[y *8 / 10**6 for y in y]
			a=[]
			b=[]
			while i< len(x):
				temp=x[i]
				sum=1
				while i < len(x)-1:
					if (x[i+1]-temp<0.011):
						i=i+1
						sum=sum+1
					else:
						break
				if (i==len(x)):
					i=i-1
				a.append(x[i])
				b.append(sum*1024)
				i=i+1
				'''
					i=1
					while i<len(b):
						if (a[i]-a[i-1]>1):
							b.insert(i,0)
							a.insert(i,a[i-1]+random.uniform(0.00001, 0.5))
							i=i+1
							b.insert(i,0)
							a.insert(i,a[i]-random.uniform(0.0000001, 0.5))
							i=i+1
						i=i+1
					'''
					#if (key == 'L2'):
					#    y=[y *1.0 for y in y]
					#plt.ylim(0, 3)
					#b=signal.lfilter(b1, a1, signal.lfilter(b1, a1, b))
			i=1
			while i<len(b):
				if (a[i]-a[i-1]>1):
					b.insert(i,0)
					a.insert(i,a[i-1]+random.uniform(0.00001, 0.5))
					i=i+1
					b.insert(i,0)
					a.insert(i,a[i]-random.uniform(0.0000001, 0.5))
					i=i+1
				i=i+1
			b=signal.lfilter(b1, a1, signal.lfilter(b1, a1, b))
			b=[b / 2500 for b in b]


			if (key=='F1'):
				plt.plot(a,b,'k.',label=key)
			if (key=='F2'):
				plt.plot(a,b,'r.',label=key)
			if (key=='F3'):
				plt.plot(a,b,'g.',label=key)
		#And do the plotting
		axes.legend()
		plt.show()

	def packet_delay_graph(self, case, descriptor):
		b, a = signal.butter(2, 0.03)
		figure, axes=plt.subplots()
		title='Packet Delay:   Case ' + str(case)
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#now printing out the dictionary as plot
		for key in logger.table.table_packet_delay:
			#print logger.table.table_packet_delay[key]
			x=logger.table.clock_packet_delay[key]
			x.insert(0,0)
			y=logger.table.table_packet_delay[key]
			y.insert(0,0)
			y2 = signal.lfilter(b, a, signal.lfilter(b,a,y))
			y.insert(0,0)
			plt.plot(x,y2,label=key)
		#And do the plotting
		axes.legend()
		plt.show()
	
	def packet_loss_graph(self, case, descriptor):
		figure, axes=plt.subplots()
		title='Packet Loss:   Case ' + str(case)
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#now printing out the dictionary as plot
		for key in logger.table.table_packet_loss:
			#print logger.table.table_window[key]
			
			x=logger.table.clock_packet_loss[key]
			a=[]
			b=[]
			i=0
			while i< len(x):
				temp=x[i]
				sum=1
				while i < len(x)-1:
					if (x[i+1]-temp<1):
						i=i+1
						sum=sum+1
					else:
						break
				if (i==len(x)):
					i=i-1
						
				a.append(x[i])
				b.append(sum)
				i=i+1
			#plt.plot(a, b,label=key)
			b=[b / 10 for b in b]
			if key== 'L1':
				plt.plot(a,b,'go',label=key)
			if key== 'L2':
				plt.plot(a,b,'r*',label=key)
			if key== 'L3':
				plt.plot(a,b,'bx',label=key)

			

			
			#plt.plot(logger.table.clock_packet_loss[key], logger.table.table_packet_loss[key],'o',label=key)
		#And do the plotting
		axes.legend()
		plt.show()

	def window_size_graph(self, case, descriptor):
		figure, axes=plt.subplots()
		b, a = signal.butter(2, 0.03)
		title='Window Size:   Case ' + str(case) 
		figure.canvas.set_window_title(title)
		axes.set_title(title)
		axes.set_xlabel('Time in Second')
		axes.set_ylabel(descriptor)
		#now printing out the dictionary as plot
		for key in logger.table.table_window:
			x=logger.table.clock_window[key]
			y=logger.table.table_window[key]
			x.insert(0,0)
			y.insert(0,0)
			plt.plot(x, y,label=key)
		#And do the plotting
		axes.legend()
		plt.show()





"""
logger.table.buff_occupancy_log("ABC",1)
logger.table.clock_log(0.1)
logger.table.buff_occupancy_log("ABC",2) 
logger.table.clock_log(0.2)
logger.table.buff_occupancy_log("ABC",4) 
logger.table.clock_log(0.3)
logger.table.buff_occupancy_log("ABC",5) 
logger.table.clock_log(0.4)
logger.table.buff_occupancy_log("ABC",6) 
logger.table.clock_log(0.5)

"""

"""
clock.clk.update_time(0.0)
logger.table.link_rate_log("ABC",1)
logger.table.link_rate_log("C",2)
clock.clk.update_time(0.1)
logger.table.link_rate_log("ABC",0.1)
logger.table.link_rate_log("C",0.2)
clock.clk.update_time(0.2)
logger.table.link_rate_log("ABC",4)
logger.table.link_rate_log("C",8)
clock.clk.update_time(0.3)
logger.table.link_rate_log("ABC",2)
logger.table.link_rate_log("C",4)
clock.clk.update_time(0.4)
logger.table.link_rate_log("ABC",12)
logger.table.link_rate_log("C",14)
clock.clk.update_time(0.5)
"""




g=Graph()




#g.link_rate_graph(1,'hello')


