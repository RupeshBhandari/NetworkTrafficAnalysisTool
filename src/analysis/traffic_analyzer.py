import sqlite3
import pandas as pd
import os
from typing import Dict
import matplotlib.pyplot as plt
from capture.network_interface import NetworkInterface

class TrafficAnalyzer:
    def __init__(self):
        self.network_interfaces: Dict[str, NetworkInterface] = {}
        self.db_path = os.path.join('data', 'traffic_data.db')

        # Initialize SQLite database and table
        self._initialize_database()

    def _initialize_database(self):
        # Create a SQLite connection and cursor
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source_ip TEXT,
                destination_ip TEXT,
                protocol TEXT,
                size INTEGER
            )
        ''')
        self.conn.commit()

    def add_interface(self, name: str):
        interface = NetworkInterface(name)
        self.network_interfaces[name] = interface

    def start_capture(self, interface_name: str, duration: int):
        if interface_name in self.network_interfaces:
            self.network_interfaces[interface_name].start_capture(duration)
            self.store_data(interface_name)
        else:
            raise ValueError("Interface not found")

    def store_data(self, interface_name: str):
        if interface_name not in self.network_interfaces:
            raise ValueError("Interface not found")

        interface = self.network_interfaces[interface_name]
        packets = interface.get_packets()
        raw_df = pd.DataFrame([vars(pkt) for pkt in packets])

        # Store data in SQLite
        raw_df.to_sql('packets', self.conn, if_exists='append', index=False)

    def analyze_traffic(self) -> str:
        # Fetch data from SQLite for analysis
        query = "SELECT * FROM packets"
        raw_df = pd.read_sql(query, self.conn)

        if raw_df.empty:
            return "# Traffic Analysis Report\n\nNo data captured.\n"

        total_traffic = raw_df['size'].sum()
        protocol_distribution = raw_df['protocol'].value_counts()
        top_sources = raw_df['source_ip'].value_counts().head(10)
        top_destinations = raw_df['destination_ip'].value_counts().head(10)
        average_packet_size = raw_df['size'].mean()

        # Pretty dividers
        divider = "════════════════════════════════════════════\n"
        short_divider = "────────────────────────────────────────────\n"

        # Generate markdown report
        markdown_report = f"# Traffic Analysis Report\n\n"
        markdown_report += divider
        markdown_report += f"## Summary\n\n"
        markdown_report += f"- Total Traffic: {total_traffic} bytes\n"
        markdown_report += f"- Average Packet Size: {average_packet_size:.2f} bytes\n"
        markdown_report += f"- Total Packets Captured: {len(raw_df)}\n\n"
        markdown_report += divider

        markdown_report += f"## Protocol Distribution\n\n"
        markdown_report += protocol_distribution.to_markdown() + "\n\n"
        markdown_report += divider

        markdown_report += f"## Top Source IPs\n\n"
        markdown_report += top_sources.to_markdown() + "\n\n"
        markdown_report += divider

        markdown_report += f"## Top Destination IPs\n\n"
        markdown_report += top_destinations.to_markdown() + "\n\n"
        markdown_report += divider

        return markdown_report

    def visualize_traffic(self):
        # Fetch data from SQLite for visualization
        query = "SELECT * FROM packets"
        raw_df = pd.read_sql(query, self.conn)

        if raw_df.empty:
            print("No data to visualize.")
            return

        protocol_distribution = raw_df['protocol'].value_counts()
        top_sources = raw_df['source_ip'].value_counts().head(10)
        top_destinations = raw_df['destination_ip'].value_counts().head(10)

        plt.figure(figsize=(10, 6))

        # Plot Protocol Distribution
        plt.subplot(3, 1, 1)
        protocol_distribution.plot(kind='bar', color='skyblue')
        plt.title('Protocol Distribution')
        plt.xlabel('Protocol')
        plt.ylabel('Count')

        # Plot Top Source IPs
        plt.subplot(3, 1, 2)
        top_sources.plot(kind='bar', color='salmon')
        plt.title('Top Source IPs')
        plt.xlabel('Source IP')
        plt.ylabel('Count')

        # Plot Top Destination IPs
        plt.subplot(3, 1, 3)
        top_destinations.plot(kind='bar', color='lightgreen')
        plt.title('Top Destination IPs')
        plt.xlabel('Destination IP')
        plt.ylabel('Count')

        plt.tight_layout()
        plt.show()

    def __del__(self):
        # Close the SQLite connection when the object is destroyed
        self.conn.close()
