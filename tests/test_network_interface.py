import unittest, sys, os
import time  # Import time to add sleep
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.capture.network_interface import NetworkInterface  # Adjust the import based on your module structure

class TestNetworkInterface(unittest.TestCase):

    def setUp(self):
        # Setup code, runs before each test method
        self.interface_name = "Wi-Fi"
        self.network_interface = NetworkInterface(name=self.interface_name, capture_duration=20, packet_filter="TCP")

    def test_initialization(self):
        # Test the initialization of the NetworkInterface
        self.assertEqual(self.network_interface.name, 'Wi-Fi')
        self.assertEqual(self.network_interface.capture_duration, 20)
        self.assertEqual(self.network_interface.packet_filter, "TCP")
        self.assertEqual(len(self.network_interface.packets), 0)

    def test_start_capture(self):
        # Test the start_capture method
        try:
            self.network_interface.start_capture(duration=2)  # Capture for 2 seconds
            self.assertTrue(self.network_interface.is_capturing, "Capture should be in progress")
            time.sleep(3)  # Wait for capture to complete
        except Exception as e:
            self.fail(f"start_capture raised an exception: {e}")

        # Check that capturing stopped and packets were captured
        self.assertFalse(self.network_interface.is_capturing, "Capture should have stopped")
        self.assertGreater(len(self.network_interface.packets), 0, "Packets should have been captured")

    def test_stop_capture(self):
        # Test the stop_capture method
        self.network_interface.start_capture(duration=10)  # Start capture
        result = self.network_interface.stop_capture()  # Stop capture immediately
        self.assertFalse(self.network_interface.is_capturing, "Capture should be stopped")
        self.assertEqual(result, "Capture stopped", "stop_capture should return 'Capture stopped'")

    def test_get_packets(self):
        # Test the get_packets method
        self.network_interface.start_capture(duration=2)  # Capture for 2 seconds
        time.sleep(3)  # Wait for capture to complete
        packets = self.network_interface.get_packets()
        self.assertEqual(packets, self.network_interface.packets, "get_packets should return the captured packets")

if __name__ == '__main__':
    unittest.main()
