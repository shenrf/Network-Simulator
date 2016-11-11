import json
packet_num=0
class Flow:
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
       # jsonObject=json.load(file('testcase1.json'))
       # flow={}
       # for l in jsonObject['flows']:
       #     flow[l['id']]=Flow(l)
       # l1=fow.get('F1')
   

# we have 2 types of packets:
#     1) data_packet, which sends data
#     2) Ack_packet, which sends the acknlowedge data 

class Data_Packet:
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
