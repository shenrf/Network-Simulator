from flow import Data_Packet,Ack_Packet
class Device:
    def __init__(self, id):
        self.id = id;

    def attach_link(self, link):
        return

    def handle_packet(self, packet):
        return


class Host(Device):
    def __init__(self, id):
        Device.__init__(self, id)
        self.link = None
        self.flow = {}
        self.data_packet_tracker = {}
        self.event_scheduler = None

    def attach_link(self, link):
        if self.link == None:
            self.link = link

    # def data_received(self, packet):
        # if packet.flow_id not in self.data_packet_tracker
        #   self.data_packet_tracker[flow_id] = Packet_Tracker
        # ack_tracker = self.data_packet_tracker[packet.flow_id];
        # ack_tracker.account_for_packet(packet.packet_id)
        # return packet.acknowledgement(ack_tracker.next_packet)

    def handle_packet(self, packet):
        if isinstance(packet, Data_Packet): # if it is a data packet, construct ack
            ack_packet = packet.send_ack_packet()
            self.link.send(ack_packet, self)
        elif isinstance(packet, Ack_Packet):    # if it is an ack, tell the flow that the ack has been received
            self.flow[packet.flow_id].receive_ack(packet)


    def send(self, packet):
        # assert packet.source = self
        self.link.send(packet, self)

# def send_routing_packet()     # updated in link?

