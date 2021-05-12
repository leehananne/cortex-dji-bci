# -*- encoding: utf-8 -*-
import socket

ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind with the IP broadcasting port.
ip_sock.bind(('0.0.0.0', 40926))

# Wait to receive data.
ip_str = ip_sock.recvfrom(1024)

# Output the data.
print(ip_str)