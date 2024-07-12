from datetime import datetime

class Packet:
    def __init__(self, timestamp: datetime, source_ip: str, destination_ip: str, protocol: str, size: int):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.protocol = protocol
        self.size = size

    def __str__(self) -> str:
        return (f"Packet(timestamp={self.timestamp}, source_ip={self.source_ip}, "
                f"destination_ip={self.destination_ip}, protocol={self.protocol}, size={self.size})")
