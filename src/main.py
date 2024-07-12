import time
import yaml
import logging
from capture.network_interface import NetworkInterface
from analysis.traffic_analyzer import TrafficAnalyzer

# Function to load configuration from config.yaml
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Function to initialize logging
def setup_logging(log_file):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("logs/app.log")])

def main():
    # Load configuration from config.yaml
    config = load_config('config/config.yaml')
    interface_name = config['network_interface']['name']
    capture_duration = config['network_interface']['capture_duration']
    packet_filter = config['network_interface']['packet_filter']
    log_file_path = config['logging']['file_path']

    # Setup logging
    setup_logging(log_file_path)
    logging.info(f"Starting packet capture on interface: {interface_name}")

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
