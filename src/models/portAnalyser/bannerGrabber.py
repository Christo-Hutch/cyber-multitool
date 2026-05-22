import socket
import json

class BannerGrabber:
    def __init__(self, target: str):
        self.target = target
        self.probe_dict = self.get_probe_dict()

    @staticmethod
    def get_probe_dict():
        with open("src/config/port_probes.json", "r") as f:
            return json.load(f)

    def get_probe(self, port: int):
        probe_config = self.probe_dict.get(str(port), self.probe_dict.get("default", {"payload": "\r\n"}))
        raw_payload = probe_config.get("payload", "\r\n")
        
        return raw_payload.encode('utf-8').decode('unicode_escape').encode('latin-1')

    def banner_grabber(self, port: int):
        with socket.create_connection((self.target, port), timeout=3.0) as sock:
            try:
                sock.sendall(self.get_probe(port))
                response_bytes = sock.recv(1024)

                if not response_bytes:
                    return "[EMPTY RESPONSE]"
                
                return response_bytes
            
            except TimeoutError:
                print(f"TIMED OUT: Port {port} didn't respond in time!")
            except ConnectionRefusedError:
                print(f"REFUSED: Port {port} closed or rejected connection!")
            except Exception as e:
                print(f"ERROR: Port {port} - {e}")
            
            return None