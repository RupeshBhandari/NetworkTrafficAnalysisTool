from typing import List
from scapy.all import sniff, IP
from datetime import datetime
from .packet import Packet

class NetworkInterface:
    def __init__(self, name: str, capture_duration: int = 10, packet_filter: str = ""):
        """
        Initialize a NetworkInterface instance.

        :param name: The name of the network interface
        :param capture_duration: The duration to capture packets in seconds (default is 10 seconds)
        :param packet_filter: The filter string to specify which packets to capture (default is "")
        """
        self.name = name
        self.packets: List[Packet] = []
        self.capture_duration = capture_duration
        self.is_capturing = False
        self.packet_filter = packet_filter

    def start_capture(self, duration: int = 10):
        if self.is_capturing:
            raise BufferError("Capturing in progress")

        self.is_capturing = True

        def packet_handler(packet):
            if IP in packet:
                protocol = packet[IP].proto
                proto = "TCP" if protocol == 6 else "UDP" if protocol == 17 else "Other"
                pkt = Packet(datetime.now(), packet[IP].src, packet[IP].dst, proto, len(packet))
                self.packets.append(pkt)

        try:
            sniff(iface=self.name, prn=packet_handler, store=0, timeout=duration)
        finally:
            self.is_capturing = False

    def stop_capture(self):
        if not self.is_capturing:
            return "No capture in progress"
        
        self.is_capturing = False
        return "Capture stopped"

    def get_packets(self) -> List[Packet]:
        return self.packets
