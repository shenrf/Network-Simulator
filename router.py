from device import Device
from flow import Router_Packet, Ack_Packet, Data_Packet

class RoutingTable():
    def __init__(self):
        self._table = {}    # dict
    
    def get_entry(self, device_id):
        if device_id in self._table:
            return self._table[device_id]  # device_id -> (link, delay)
        else:
            return None

    def set_up_table(self, device_id, link, delay):
        if device_id not in self._table:
            self._table[device_id] = (link, delay)
            return True
        elif self._table[device_id][1] > delay:
            self._table[device_id] = (link, delay)
            return True
        return False



'''
    def update_entry(self, host_id, link):
        if host_id not in self._table:
            self._table[host_id] = (timestamp, link)
            return True
        else:
            if timestamp > self._table[host_id][0]:
                self._table[host_id] = (timestamp, link)
                return True
            else:
                return False
'''



class Router(Device):
    def __init__(self, id):
        Device.__init__(self, id)
        self.routing_table = RoutingTable()
        self.links = []     # list
    
    def __str__(self):
        return "Router ID  " + str(self.id) + "\n"
    
    
    def attach_link(self, link):
        self.links.append(link)
    
    
    # update routing table
    def _handle_routing_packet(self, packet):
        if (self.routing_table.set_up_table(packet.source.id, packet.link, packet.delay) == True):
            for att_link in self.links:
                if att_link.id != packet.link.id:
                    packet.delay = self.routing_table.get_entry(packet.source.id)[1] + att_link.delay
                    att_link.send(packet, self)
        return True


    # handle data packet or ack packet
    def _handle_data_ack_packet(self, packet):
        # looking up the routing table and forward the packet to next device
        link = self.routing_table.get_entry(packet.destination.id)[0]
        link.send(packet, self)
    
        # what if destination not found in routing table??????
    
    
    def handle_packet(self, packet):
        if isinstance(packet, Data_Packet) or isinstance(packet, Ack_Packet):
            self._handle_data_ack_packet(packet)
        elif isinstance(packet, Router_Packet):
            self._handle_routing_packet(packet)

