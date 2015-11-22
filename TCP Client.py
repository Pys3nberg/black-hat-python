import socket

target_host = '0.0.0.0'
target_port = 6666

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#   Connect the client
client.connect((target_host, target_port))

# Send some data
client.send(b"Hello")

# Recieve sme data
response = client.recv(4096)

print(response)