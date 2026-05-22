import math
import socket
import threading
from queue import Queue

class PortScanner:
    def __init__(self, target: str, port_range: tuple):
        self.target = target
        self.port_queue = self.fill_port_queue(port_range)
        self.open_ports = []

    def fill_port_queue(self, port_range: tuple) -> Queue:
        queue = Queue()

        for port_num in range(port_range[0], port_range[1] + 1):
            queue.put(port_num)

        return queue

    def port_scan(self, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect_ex((self.target, port))
            sock.connect((self.target, port))
            return True
        
        except:
            return False
    
    def scan_port_queue(self):
        while not self.port_queue.empty():
            port_num = self.port_queue.get()
            if self.port_scan(port_num):
                print(f"Port {port_num} is open!")
                self.open_ports.append(port_num)

    def get_open_ports(self) -> list:
        thread_list = []

        thread_count = math.ceil(self.port_queue._qsize() / 10)

        for t in range(thread_count):
            thread = threading.Thread(target=self.scan_port_queue)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        return self.open_ports