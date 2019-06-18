import scapy.all as sp


class TCPDumpHelper:

    def __init__(self, path):
        self.packets = sp.rdpcap(path)
        # Let's iterate through every packet
        for packet in self.packets:
            # We're only interested packets with a DNS Round Robin layer
            packet.summary()
