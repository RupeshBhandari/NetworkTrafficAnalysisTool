import time
import logging
from capture.network_interface import NetworkInterface
from analysis.traffic_analyzer import TrafficAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("logs/app.log")])

def main():
    interface_name = "Wi-Fi"  # Replace with the actual name of your network interface
    capture_duration = 20  # Duration to capture packets in seconds

    # Initialize Network Interface and Traffic Analyzer
    logging.info("Initializing network interface and traffic analyzer.")
    network_interface = NetworkInterface(name=interface_name, capture_duration=capture_duration)
    traffic_analyzer = TrafficAnalyzer()

    # Add the network interface to the analyzer
    traffic_analyzer.add_interface(interface_name)

    try:
        while True:
            # Start capturing packets
            logging.info(f"Starting packet capture on interface: {interface_name} for {capture_duration} seconds.")
            traffic_analyzer.start_capture(interface_name, duration=capture_duration)
            logging.info("Packet capture completed.")

            # Analyze the captured traffic
            logging.info("Analyzing captured traffic...")
            analysis_report = traffic_analyzer.analyze_traffic(interface_name)

            # Display analysis report
            logging.info("Traffic Analysis Report:")
            print(analysis_report)

            # Visualize the traffic data
            logging.info("Visualizing traffic data...")
            traffic_analyzer.visualize_traffic(interface_name)

            # Sleep before next capture
            logging.info(f"Sleeping for {capture_duration} seconds before next capture.")
            time.sleep(capture_duration)

    except KeyboardInterrupt:
        logging.info("Exiting the program...")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
