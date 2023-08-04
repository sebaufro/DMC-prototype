import socket
import ipaddress

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def checkCentralRef(ip):
    new_ip = None
    if ip is None:
        new_ip = get_ip_address()
    else:
        try:
            new_ip = ipaddress.ip_address(ip)
            new_ip = ip
        except:
            print('invalid ip, using local ip')

    return new_ip