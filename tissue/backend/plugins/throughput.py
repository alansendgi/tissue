from collections import defaultdict
import socket as sock

from scapy.all import *
from yapsy.IPlugin import IPlugin


class ThroughputPlugin():
    def __init__(self):
        self.stats = defaultdict(int)

    def update(self):
        packets = get_streams(self.iface)
        throughput_data = defaultdict(int)
        for packet in packets:
            IP_layer = packet.getlayer('IP')
            throughput_data[IP_layer.dst] += IP_layer.len

        results = [('THROUGHPUT-DATA', throughput_data.items())]
        return results

    def getInformation(self, iface):
        self.iface = iface

        with open('plugins/throughput.js', 'r') as content_file:
            content = content_file.read()
        return {
            'MainClass': 'ThroughputChart',
            'Code': content,
            'GridWidth': 1,
            'GridHeight': 1
        }


def get_local_ip():
    return sock.gethostbyname(socket.gethostname())


def get_streams(iface):
    return sniff(iface='eth0', filter='tcp and src %s' % get_local_ip(), count=10)
