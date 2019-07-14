import scapy.all as sp
import datetime as dt


class TCPDumpHelper:

    def __init__(self, p):
        self.path = p
        # with Jan 1 1970 as reference, the exp_day is the no of seconds till experiment day
        self.exp_day = 1539388800
        self.Mac_IP_Map = dict()
        self.Mac_IP_Map['e8:4e:06:24:e8:e4'] = "10.10.10.5"
        self.Mac_IP_Map['bc:30:7e:07:97:ce'] = "10.10.10.40"
        self.Mac_IP_Map['00:1b:b1:b1:62:56'] = "10.10.10.50"
        self.Mac_IP_Map['00:80:48:6b:fd:16'] = "10.10.10.70"
        self.Mac_IP_Map['40:b8:9a:f7:42:dd'] = "10.10.10.71"
        self.Mac_IP_Map['00:0b:6b:02:0c:2e'] = "10.10.10.80"
        self.Mac_IP_Map['70:77:81:31:c0:3f'] = "10.10.10.81"
        self.Mac_IP_Map['ac:d1:b8:cf:a4:e1'] = "10.10.10.82"
        self.Mac_IP_Map['00:1b:b1:b1:62:4a'] = "10.10.10.90"
        self.Mac_IP_Map['60:6d:c7:4b:a7:f1'] = "10.10.10.91"
        self.Mac_IP_Map['d8:5d:e2:ab:e2:5f'] = "10.10.10.92"
        self.Mac_IP_Map['00:80:48:6b:fd:17'] = "10.10.10.100"
        self.Mac_IP_Map['10:08:b1:d1:f6:b3'] = "10.10.10.102"

        self.IP_Mac_Map = dict()
        self.IP_Mac_Map['10.10.10.5'] = "e8:4e:06:24:e8:e4"
        self.IP_Mac_Map['10.10.10.40'] = "bc:30:7e:07:97:ce"
        self.IP_Mac_Map['10.10.10.50'] = "00:1b:b1:b1:62:56"
        self.IP_Mac_Map['10.10.10.70'] = "00:80:48:6b:fd:16"
        self.IP_Mac_Map['10.10.10.71'] = "40:b8:9a:f7:42:dd"
        self.IP_Mac_Map['10.10.10.80'] = "00:0b:6b:02:0c:2e"
        self.IP_Mac_Map['10.10.10.81'] = "70:77:81:31:c0:3f"
        self.IP_Mac_Map['10.10.10.82'] = "ac:d1:b8:cf:a4:e1"
        self.IP_Mac_Map['10.10.10.90'] = "00:1b:b1:b1:62:4a"
        self.IP_Mac_Map['10.10.10.91'] = "60:6d:c7:4b:a7:f1"
        self.IP_Mac_Map['10.10.10.92'] = "d8:5d:e2:ab:e2:5f"
        self.IP_Mac_Map['10.10.10.100'] = "00:80:48:6b:fd:17"
        self.IP_Mac_Map['10.10.10.102'] = "10:08:b1:d1:f6:b3"
        self.IP_Mac_Map['all'] = "ff:ff:ff:ff:ff:ff"

    def export_signal_strength(self, src_ip, save_path):
        is_all = src_ip == 'all'
        with open(save_path, 'w') as f:
            f.write("Src IP,Transmit Mac, Transmit IP, Dst IP,"
                    "Signal Strength, Time of the day, Raw time (seconds), Micros\n")
            for packet in sp.PcapReader(self.path):
                dels_sec = packet.time - self.exp_day
                dels_mins = dels_sec / 60
                secs = dels_sec % 60
                micro = int((secs - int(secs)) * 10 ** 6)
                secs = int(secs)
                mins = int(dels_mins % 60)
                hours = int(dels_mins / 60)
                timestamp = dt.datetime(year=2018, month=10, day=13, hour=hours, minute=mins,
                                        second=int(secs), microsecond=micro)
                if packet.haslayer(sp.IP) and packet.haslayer(sp.RadioTap):
                    if packet[sp.Dot11].fields['addr2'] == self.IP_Mac_Map[src_ip] or is_all:
                        f.write(packet[sp.IP].fields['src'] + "," + packet[sp.Dot11].fields['addr2']
                                + "," + src_ip + "," + packet[sp.IP].fields['dst'] + ","
                                + str(packet[sp.RadioTap].fields['dBm_AntSignal']) + "," + str(timestamp) +
                                "," + str(packet.time) + "," + str(int(micro)) + "\n")

    def export_inter_arrival_time(self, save_path):
        old = 0
        with open(save_path, 'w') as f:
            f.write("Time (milli), Time of the day, Raw time (seconds), Micros\n")
            for packet in sp.PcapReader(self.path):
                dels_sec = packet.time - self.exp_day
                dels_mins = dels_sec / 60
                secs = dels_sec % 60
                micro = int((secs - int(secs)) * 10 ** 6)
                secs = int(secs)
                mins = int(dels_mins % 60)
                hours = int(dels_mins / 60)
                timestamp = dt.datetime(year=2018, month=10, day=13, hour=hours, minute=mins,
                                        second=int(secs), microsecond=micro)

                delta = packet.time - old
                delta = delta * 1000
                old = packet.time
                f.write(str(delta)+","+str(timestamp)+","+str(packet.time) + "," + str(int(micro)) + "\n")
