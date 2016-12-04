import clock
#from link import Link 
#from flow import Data_Packet, Ack_Packet, Router_Packet
from event import Event,FlowWakeEvent
from event_queue import EventQueue
slow_start = "Slow Start"
congestion_avoidance = "Congestion Avoidance"
fast_recovery = "Fast Recovery"

class CongestionControllerReno(CongestionController):
	def __init__(self,flow):
		self.state = slow_start
		self.FR_packet = None
		self.flow=flow
	# process the ack
	def ack_received(self, packet):
		# check for timed-out unacknowledge packets
		for (packet_id, dup_num) in self.no_ack.keys():
			send_time = self.no_ack[(packet_id, dup_num)]
			time_diff = clock.clk.get_time() - send_time 	# need current time!!!!
			if time_diff > self.timeout:
				del self.no_ack[(packet_id, dup_num)]
				self.time_out.append((packet_id, dup_num))

		# setup for retransmission
		if len(self.time_out) > 0:
			self.retransmit = True
			self.cwnd /= 2
		else:
			self.retransmit = False

		if self.wake_event != None:
			self.event_scheduler.cancel_event(self.wake_event)

		# delete acknowledged packet
		if (packet.id, packet.dup_num) in self.no_ack.keys():
			del self.no_ack[(packet_id, dup_num)]

		if self.state == slow_start:
			self.cwnd += 1
			if self.cwnd >= self.ssthresh:
				self.state == congestion_avoidance
		elif self.state == congestion_avoidance:
			if packet.next_id == self.last_received_ack:
				self.dup_count += 1
				if (self.dup_count == 3) and (packet.next_id in [key[0] for key in self.no_ack.keys()]):
					self.cwnd /= 2
					self.ssthresh = self.cwnd
					self.state = fast_recovery
			else:
				self.cwnd += 1 / self.cwnd
				self.dup_count = 0
		elif self.state == fast_recovery:
			if packet.next_id == self.last_received_ack:
				self.dup_count += 1
				self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))
				return
			else:
				if packet.id == self.FR_packet:
					self.cwnd = ssthresh
					self.state = congestion_avoidance
				self.dup_count = 0
		self.last_received_ack = packet.next_id
		self.send_packet()
		self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))


	def send_packet(self):
		if self.state == slow_start or self.state == congestion_avoidance:
			if self.retransmit == True:
				while (len(self.no_ack) < self.cwnd) and (len(self.time_out) > 0):
					(packet_id, dup_num) = self.time_out[0]
					self.no_ack[(packet_id, dup_num + 1)] = clock.clk.get_time()		# clock!!!
					self.flow.send_data_packet(packet_id, dup_num)	# flow.send!!!!
					del self.time_out[0]
			else:
				while (len(self.no_ack) < self.cwnd):
					self.no_ack[(window_start, 0)] = clock.clk.get_time()
					self.flow.send_data_packet(window_start, 0)
					window_start += 1
		else:
			packet_id = self.last_received_ack
			self.FR_packet = packet_id
			for key in self.no_ack.keys():
				if key[0] == packet_id:
					keys.append(key)
			if len(keys) == 1:
				dup_num = keys[0][1]
				del self.no_ack[(packet_id, dup_num)]
				self.no_ack[(packet_id, dup_num + 1)] = clock.clk.get_time()
				self.flow.send_data_packet(packet_id, dup_num + 1)


	def wake(self):
		if self.state == fast_recovery:
			self.state == slow_start
		else:
			self.cwnd/= 2

		for (packet_id, dup_num) in self.no_ack.keys():
			send_time = self.no_ack[(packet_id, dup_num)]
			time_diff = clock.clk.get_time() - send_time
			if time_diff > self.timeout:
				del self.no_ack[(packet_id, dup_num)]
				self.timed_out.append((packet_id, dup_num))
		if len(self.timed_out) > 0:
			self.retransmit = True
		else:
			self.retransmit = False   
		self.send_packet()
		self.wake_event = self.event_scheduler.put_event(self.timeout, FlowWakeEvent(self.flow))  
		print "cwnd: ", str(cwnd)
		
	def __str__(self):
		return ("ssthresh:       " + str(self.ssthresh) + "\n"
				"cwnd:           " + str(self.cwnd) + "\n"
				"duplicate ACKS: " + str(self.dup_count) + "\n")    