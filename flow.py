import json
from math import pow
from packet_tracker import PacketTracker
from fasttcp import CongestionControllerFast,CongestionControllerReno
packet_num=0
amount=0
class Flow:
<<<<<<< HEAD
	"""   -id =the identifier of the flow object;
		-source = node that send outs the packets;
		-destination = be the destination of each packets;
		-size = be the data amount in B (byte)
		-start = the start time of the flow process
		"""
	num=0
	def __init__(self, flowObject):
		self.event_queue=None
		num=0
		self.id = flowObject['id']
		self.source = None
		self.destination = None
		self.size = 1024 # size of one data packet 1024B
		self.total_amount=flowObject['amount'] # total size to transmit 20MB
		self.start_time = flowObject['start']
		self.ack_tracker=PacketTracker()
		self.controller=CongestionControllerFast(self)
		self.controller.event_scheduler=self.event_queue
	def __str__(self):
		return ('Flow that coming from' + self.source + 'to: ' + self.destination)
	def runTime(self):
		return __str__(self.start_time)
	
	def send_data_packet(self,packet_id, dup_num):
		# 20MB/1024B =19532
		#amount=self.total_amount/self.size #change here, correct value should be 19532
		#amount=self.total_amount/self.size # the number of total packets
		#print packet_id
		temp = Data_Packet(packet_id, self.id,self.source, self.destination, self.size,dup_num)
		#packet_num=packet_num+1
		self.source.send(temp)

	'''def send_the_rest_data_packet(self):
		global packet_num
		Flow.num=Flow.num+1
		temp = Data_Packet(packet_num, self.id,self.source, self.destination, self.size)
		packet_num=packet_num+1
		self.source.send(temp)
	'''
	'''def send_ack_packet(self):
		global packet_num
		number_of_ack_count=1; #change here, correct value should be 64
		print number_of_ack_count
		while number_of_ack_count > 0:
			num=num+1
			temp = Ack_Packet(Flow.packet_num, self.id, self.source, self.destination, 64)
			packet_num=packet_num+1
			self.source.send(temp)
			number_of_ack_count=number_of_ack_count-1;
	'''
	# def send_packet_now(self, packet_id)
	
	def receive_ack(self, packet):
		#print packet.id
		print "ACK:"+str(packet.id)
		self.ack_tracker.handler(packet)
		self.controller.ack_received(packet)
		assert isinstance(packet, Ack_Packet)
		assert packet.source == self.destination
		assert packet.destination == self.source



	if __name__ == "__main__":
		print ("Hi")
=======
<<<<<<< HEAD
    """   -id =the identifier of the flow object;
        -source = node that send outs the packets;
        -destination = be the destination of each packets;
        -size = be the data amount in bytes that we send the packets;
        -start = the start time of the flow process
        """
    num=0
    def __init__(self, flowObject):
        num=0
        self.id = flowObject['id']
        self.source = None
        self.destination = None
        self.size = flowObject['amount']
        self.start_time = flowObject['start']
    
    def __str__(self):
        return ('Flow that coming from' + self.source + 'to: ' + self.destination)
    def runTime(self):
        return __str__(self.start_time)
    
    def send_data_packet(self):
        global packet_num
        Flow.num=Flow.num+1
        temp = Data_Packet(packet_num, self.id,self.source, self.destination, self.size)
        packet_num=packet_num+1
        self.source.send(temp)
    
    def send_ack_packet(self):
        num=num+1
        temp = Ack_Packet(Flow.packet_num, self.id, self.source, self.destination, self.size)
        global packet_num
        packet_num=packet_num+1
        self.source.send(temp)
    
    # def send_packet_now(self, packet_id)
    
    def receive_ack(self, packet):
        assert isinstance(packet, Ack_Packet)
        assert packet.source == self.source
        assert packet.destination == self.destination
    
    if __name__ == "__main__":
        print ("Hi")
>>>>>>> origin/master
# jsonObject=json.load(file('testcase1.json'))
# flow={}
# for l in jsonObject['flows']:
#     flow[l['id']]=Flow(l)
# l1=fow.get('F1')


# we have 2 types of packets:
#     1) data_packet, which sends data
#     2) Ack_packet, which sends the acknlowedge data

class Data_Packet:
<<<<<<< HEAD
	def __init__(self, packet_id, flow_id, source, destination, data_size,duplicate_num):
		self.id=packet_id
		self.flow_id=flow_id
		self.source=source
		self.destination=destination
		self.size=data_size
		self.duplicate_num=duplicate_num
	def __str__(self):
		return " flow_id:"+str(self.flow_id)+" source:"+str(self.source.id)+" destination:"+str(self.destination.id)+" size:"+str(self.size)
	def send_ack_packet(self, next_id):
		temp=Ack_Packet(self.flow_id, self.id, self.destination, self.source, next_id, self.duplicate_num)
		return temp


class Ack_Packet:
	def __init__(self,flow_id, id, source, destination,next_id, duplicate_num):
		self.flow_id=flow_id
		self.id=id
		#self.data_packet_id=data_packet_id
		self.source=source
		self.destination=destination
		self.size=64
		self.next_id=next_id
		self.duplicate_num=duplicate_num
class Router_Packet:
	def __init__(self, delay, source, link, size, time):
		self.delay=delay
		self.source=source
		self.size=size
		self.link=link
		self.time=time
=======
    def __init__(self, packet_id, flow_id, source, destination, data_size):
        self.id=packet_id
        self.flow_id=flow_id
        self.source=source
        self.destination=destination
        self.size=data_size
    def __str__(self):
        return " flow_id:"+str(self.flow_id)+" source:"+str(self.source.id)+" destination:"+str(self.destination.id)+" size:"+str(self.size)
    def send_ack_packet(self):
        global packet_num
        temp=Ack_Packet(self.flow_id,packet_num, self.id, self.source, self.destination, self.size)
        packet_num=packet_num+1
        return temp


class Ack_Packet:
    def __init__(self,flow_id,data_packet_id,packet_id, source, destination, data_size):
        self.flow_id=flow_id
        self.id=packet_id
        self.data_packet_id=data_packet_id
        self.source=source
        self.destination=destination
        self.size=data_size

class Router_Packet:
    def __init__(self, delay, source, size):
        self.delay=delay
        self.source=source
        self.size=size


=======
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

>>>>>>> origin/master
>>>>>>> origin/master
