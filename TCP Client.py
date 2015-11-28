import socket

target_host = '127.0.0.1'
target_port = 5678

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#   Connect the client
client.connect((target_host, target_port))

# Send some data
client.send(b"Hello")

# Recieve sme data
response = client.recv(4096)

print(response)