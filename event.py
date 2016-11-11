class Event:
    def __init__(self):
		return
    

    def perform(self):
		print "hello world"


class FlowWakeEvent(Event):
# wake up the flow to begin sending packet
	def __init__(self, flow):
    #Event.__init__(self)
		self.flow = flow

	def perform(self):
		self.flow.send_data_packet()



class LinkReadyEvent(Event):
# wake up the link to send another packet
	def __init__(self, link):
		Event.__init__(self)
		self.link = link

	def perform(self):
		self.link.wakeup()



class PacketArrivalEvent(Event):
# when a packet arrives at the end of the a link
# notify the device to handle the packet
	def __init__(self, packet, device, from_link):
		Event.__init__(self)
		self.packet = packet
		self.device = device
		self.from_link = from_link

	def perform(self):
		self.device.handle_packet(self.packet)


'''
class RoutingUpdateEvent(Event)
def __init__(self, host):


def perform(self):
'''
