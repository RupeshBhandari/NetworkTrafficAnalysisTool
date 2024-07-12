import unittest, sys, os
import time  # Import time to add sleep
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analysis.traffic_analyzer import TrafficAnalyzer  # Adjust the import based on your module structure
from src.capture.network_interface import NetworkInterface  # Adjust the import based on your module structure


class TestTrafficAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = TrafficAnalyzer()
        self.interface_name = "Wi-Fi"
        self.analyzer.add_interface(self.interface_name)

    def test_add_interface(self):
        self.assertIn(self.interface_name, self.analyzer.network_interfaces, "Interface should be added to analyzer")

    def test_start_capture(self):
        try:
            self.analyzer.start_capture(self.interface_name, duration=2)  # Capture for 2 seconds
            # Adding a short delay to let the capture start
            time.sleep(1)
            self.assertTrue(self.analyzer.network_interfaces[self.interface_name].is_capturing, "Capture should be in progress")
            time.sleep(3)  # Wait for capture to complete
        except Exception as e:
            self.fail(f"start_capture raised an exception: {e}")

        self.assertFalse(self.analyzer.network_interfaces[self.interface_name].is_capturing, "Capture should have stopped")
        self.assertGreater(len(self.analyzer.network_interfaces[self.interface_name].packets), 0, "Packets should have been captured")

    def test_analyze_traffic(self):
        # Start capture and wait for it to complete
        self.analyzer.start_capture(self.interface_name, duration=2)
        time.sleep(3)  # Wait for capture to complete

        # Perform analysis
        analysis = self.analyzer.analyze_traffic(self.interface_name)
        self.assertIn("total_traffic", analysis, "Analysis should include total traffic")
        self.assertIn("protocol_distribution", analysis, "Analysis should include protocol distribution")
        self.assertIn("top_sources", analysis, "Analysis should include top sources")

if __name__ == '__main__':
    unittest.main()
