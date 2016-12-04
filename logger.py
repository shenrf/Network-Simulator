import matplotlib.pyplot as plt
import clock

class Log:
    """ 
        recording the data
        
    """
    def __init__(self):
        self.table_clock=[]
        self.table_clock.append(0)
        self.table_buff_occupancy=dict()
        self.clock_buff_occupancy=dict()

        self.table_flow_rate=dict()
        self.clock_flow_rate=dict()


        self.table_packet_delay=dict()
        self.clock_packet_delay=dict()

        self.table_packet_loss=dict()
        self.clock_packet_loss=dict()

        self.table_window=dict()
        self.clock_window=dict()

        self.table_link_rate=dict()
        self.clock_link_rate=dict()

    def log_clear(self):
        self.table_clock=[]
        self.table_clock.append(0)
        self.table_buff_occupancy=dict()
        self.clock_buff_occupancy=dict()

        self.table_flow_rate=dict()
        self.clock_flow_rate=dict()


        self.table_packet_delay=dict()
        self.clock_packet_delay=dict()

        self.table_packet_loss=dict()
        self.clock_packet_loss=dict()

        self.table_window=dict()
        self.clock_window=dict()

        self.table_link_rate=dict()
        self.clock_link_rate=dict()


    def clock_log(self,time_val):
        self.table_clock.append(time_val)

    def buff_occupancy_log(self,link,occupancy_val, time):
        if link in self.table_buff_occupancy:
            self.table_buff_occupancy[link].append(occupancy_val)
            self.clock_buff_occupancy[link].append(time)
            #print "append" +str(occupancy_val);
        else:
            self.table_buff_occupancy[link]=[]
            self.clock_buff_occupancy[link]=[]
            self.table_buff_occupancy[link].append(occupancy_val)
            self.clock_buff_occupancy[link].append(time)
            #print link + "  initilize:  " + str(occupancy_val)
    def flow_rate_log(self,flow,packet_val, time):
        if flow in self.table_flow_rate:
            self.table_flow_rate[flow].append(packet_val)
            self.clock_flow_rate[flow].append(time)
        else:
            self.table_flow_rate[flow]=[]
            self.clock_flow_rate[flow]=[]
            self.table_flow_rate[flow].append(packet_val)
            self.clock_flow_rate[flow].append(time)
            
    def packet_delay_log(self, flow, packet_delay, time):
        if flow in self.table_packet_delay:
            self.table_packet_delay[flow].append(packet_delay)
            self.clock_packet_delay[flow].append(time)
        else:
            self.table_packet_delay[flow]=[]
            self.clock_packet_delay[flow]=[]
            self.table_packet_delay[flow].append(packet_delay)
            self.clock_packet_delay[flow].append(time)

    def packet_packet_loss_log(self, link, val, time):
        if link in self.table_packet_loss:
            self.table_packet_loss[link].append(val)
            self.clock_packet_loss[link].append(time)
        else:
            self.table_packet_loss[link]=[]
            self.clock_packet_loss[link]=[]
            self.table_packet_loss[link].append(val)
            self.clock_packet_loss[link].append(time)

    def window_log(self, flow, window_len, time):
        if flow in self.table_window:
            self.table_window[flow].append(window_len)
            self.clock_window[flow].append(time)
        else:
            self.table_window[flow]=[]
            self.clock_window[flow]=[]
            self.table_window[flow].append(window_len)
            self.clock_window[flow].append(window_len)

    def link_rate_log(self, link, rate, time):
        if link in self.table_link_rate:
            self.table_link_rate[link].append(rate)
            self.clock_link_rate[link].append(time)
        else:
            self.table_link_rate[link]=[]
            self.clock_link_rate[link]=[]
            self.table_link_rate[link].append(rate)
            self.clock_link_rate[link].append(time)

table=Log()


"""
for key in table.table_buff_occupancy:
    print key, table.table_buff_occupancy[key]

print
print "Now do the plotting"
for key in table.table_buff_occupancy:
    plt.plot(table.table_clock, table.table_buff_occupancy[key])
plt.show()
"""




