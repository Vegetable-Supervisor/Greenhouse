from ipaddress import ip_address
from urllib.parse import urlparse

class Supervisor:
    """A Vegetable Supervisor as seen by a GreenHouse."""

    def __init__(self, location):
        """Contruct a Supervisor from a location (e.g. "192.168.0.23:54")"""
        def parse_ip_port(location):
            assert location
            if location.split(":")[0] == "localhost":
                location = location.replace("localhost", "127.0.0.1", 1)
            try:
                ip = ip_address(location)
                port = None
            except ValueError:
                parsed = urlparse('//{}'.format(location))
                ip = ip_address(parsed.hostname)
                port = parsed.port
            return ip, port

        self.location = location
        self.ip, self.port = parse_ip_port(location)
