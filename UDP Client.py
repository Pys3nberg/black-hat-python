import socket

# local host ip
target_host = '127.0.0.1'
target_port = 5001

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# Recieve some data
data, addr = client.recvfrom(4096)

print(data)