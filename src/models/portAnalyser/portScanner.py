import socket

def port_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    
    except:
        return False
    
def port_scan_range(target: str, port_range: tuple):
    for port_num in range(port_range[0], port_range[1]):
        result = port_scan(target, port_num)

        if result:
            print(f"Port {port_num} is open!")

        else:
            print(f"Port {port_num} is closed!")