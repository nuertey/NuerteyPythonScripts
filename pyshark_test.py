import pyshark

test_capture = pyshark.FileCapture('test_packet_capture.pcapng')
test_capture
print(test_capture[0])

cap = pyshark.FileCapture('test_packet_capture.pcapng', display_filter="tls")
for pkt in cap:
    print(pkt.highest_layer)

def print_info_layer(packet):
    print("[Protocol:] "+packet.highest_layer+" [Source IP:] "+packet.ip.src+" [Destination IP:]"+packet.ip.dst)
cap.apply_on_packets(print_info_layer)

#live_ring_buffer_capture = pyshark.LiveRingCapture(interface='wlp2s0')
live_capture = pyshark.LiveCapture(interface='wlp2s0')
live_capture.sniff(timeout=50)
live_capture
print(live_capture[3])

for packet in live_capture.sniff_continuously(packet_count=5):
    print('Just arrived:', packet)

# We can also use the apply_on_packets() method for adding the packets to a list for counting or other processing means. Here's a script that will append all of the packets to a list and print the count. For this, create a text file called count_packets.py:
packets_array = []

def counter(*args):
    packets_array.append(args[0])

def count_packets():
    cap = pyshark.FileCapture('test_packet_capture.pcapng', keep_packets=False)
    cap.apply_on_packets(counter, timeout=10000)
    return len(packets_array)

print("Packets number:"+str(count_packets()))

for packet in packets_array:
    print(packet)

# We can use only_summaries, which will return packets in the capture object with just the summary information of each packet:
cap = pyshark.FileCapture('test_packet_capture.pcapng', only_summaries=True)
print(cap[0])

# Accessing packet data:
# 
# Data can be accessed in multiple ways. Packets are divided into layers, first you have to reach the appropriate layer and then you can select your field.
# 
# All of the following work:
# 
# >>> packet['ip'].dst
# 192.168.0.1
# >>> packet.ip.src
# 192.168.0.100
# >>> packet[2].src
# 192.168.0.100
# 
# To test whether a layer is in a packet, you can use its name:
# 
# >>> 'IP' in packet
# True
# 
# To see all possible field names, use the packet.layer.field_names attribute (i.e. packet.ip.field_names) or the autocomplete function on your interpreter.
# 
# You can also get the original binary data of a field, or a pretty description of it:
# 
# >>> p.ip.addr.showname
# Source or Destination Address: 10.0.0.10 (10.0.0.10)
# # And some new attributes as well:
# >>> p.ip.addr.int_value
# 167772170
# >>> p.ip.addr.binary_value
# '\n\x00\x00\n'
