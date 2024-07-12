import unittest
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.capture.packet import Packet

class TestPacket(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.timestamp = datetime.now()
        self.source_ip = "192.168.1.1"
        self.destination_ip = "192.168.1.2"
        self.protocol = "TCP"
        self.size = 128

        self.packet = Packet(self.timestamp, self.source_ip, self.destination_ip, self.protocol, self.size)

    def test_packet_initialization(self):
        # Test the initialization of the Packet
        self.assertEqual(self.packet.timestamp, self.timestamp)
        self.assertEqual(self.packet.source_ip, self.source_ip)
        self.assertEqual(self.packet.destination_ip, self.destination_ip)
        self.assertEqual(self.packet.protocol, self.protocol)
        self.assertEqual(self.packet.size, self.size)

    def test_packet_str_representation(self):
        # Test the string representation of the Packet, if any
        expected_str = f"Packet(timestamp={self.timestamp}, source_ip={self.source_ip}, destination_ip={self.destination_ip}, protocol={self.protocol}, size={self.size})"
        self.assertEqual(str(self.packet), expected_str)

if __name__ == '__main__':
    unittest.main()
