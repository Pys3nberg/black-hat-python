import sys, socket, optparse, threading, subprocess


# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# Create Option parser and add all of teh require options

parser = optparse.OptionParser()

parser.add_option('-l','--listen', action='store_true', dest="listen",
                  help='Listen on [port]:[port] for incoming connections')
parser.add_option('-e', '--execute',  action='store', type='string', dest='file_execute',
                  help='Execute the given file upon recieving a connection')
parser.add_option('-c', '--commandshell', action='store_true', dest='cshell',
                  help='Initialize a command shell')
parser.add_option('-u', '--upload', action='store', type='string', dest='destination',
                  help='upon recieving a connection upload a file and write to [destination]')
parser.add_option('-t', '--target', action='store', dest='target')
parser.add_option('-p', '--port', action='store', dest='port')

# Parse all options
(options, args) = parser.parse_args()

if options.listen:
    print(options.listen)

def main():

    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    if options.listen:
        listen = True
    if options.file_execute:
        execute = options.file_execute
    if options.cshell:
        command = True
    if options.destination:
        upload = True
        upload_destination = options.destination
    if options.target:
        target=options.target
    if options.port:
        port = int(options.port)

    # are we going to listen or just send data from stdin?
    # so basically we have said we are not listening, but we have supplied and ip and port, so we just connect
    # to the target and send data through command lines
    if not listen and len(target) and port>0:

        # read in the buffer from commandline
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = input().encode('utf-8')
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()

def client_sender(buffer):

    # Initialize a socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # try and connect to our target
        client.connect((target,port))
        print('connected to server on {}:{}'.format(target, port))
        if len(buffer):
            client.send(buffer)

        while True:

            # now wait for data back
            recv_len = 1
            response = b''

            while recv_len:

                # recieve a maximum of 4096 bytes, if it is less than that exit the loop and
                # handle the data, if its equal then keep recieving until you recieve less
                # than 4096 bytes in one hiit, meaning youve reached the end of teh data
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response.decode())

            # wait for more data
            buffer = input().encode('utf-8')
            if buffer == b'qq': break
            client.send(buffer)

    except:

        print('[*] Exception! Exiting.')

        # tear down the connection
        client.close()

    finally:
        print('Socket closed')
        client.close()

def server_loop():

    global target

    #if no target is defined, we listen on all inetrfaces '0.0.0.0'
    if not target:
        target='0.0.0.0'

    # init the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    print('server bound too {}:{}'.format(target, port))
    server.listen(5)

    connections = []
    while True:

        client_socket, addr = server.accept()
        print('accepted connection from {}'.format(addr))
        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket, addr))
        client_thread.start()
        connections.append(client_thread)



def client_handler(client_socket, addr):

    global upload
    global execute
    global command

    print(addr)
    # check for upload

    try:
        if upload:

            # read in all of the bytes and write to our destination
            file_buffer = b''

            # keep reading until noe is available
            while True:

                data = client_socket.recv(1024)

                client_socket.send(b'ACK')

                if data==b'q':
                    break

                else:
                    file_buffer += data

            try:

                with open(upload_destination, 'wb') as fid:
                    fid.write(file_buffer)

                client_socket.send('Successfully saved file to {}'.format(upload_destination).encode('utf-8'))

            except:
                client_socket.send('Failed to save file to {}'.format(upload_destination).encode('utf-8'))

        if len(execute):

            # run_command
            output = run_command(execute)
            client_socket.send(output)

        if command:
            print(client_socket.recv(1024))
            client_socket.send(b'<BhP:>')
            while True:

                cmd = client_socket.recv(1024)

                print(cmd)
                response = run_command(cmd.decode('utf-8'))

                client_socket.send(response)

        else:
            data = client_socket.recv(1024)
            while not data == b'q':
                client_socket.send(data)
                data = client_socket.recv(1024)

    except:
        print('Something went wrong')
        client_socket.close()

def run_command(command):

    # trim the newline
    command = command.strip()

    # run the command and get the output back

    try:

        output = subprocess.check_output(command, stderr= subprocess.STDOUT, shell=True)

    except:

        output = 'Failed to execute command.'

    # send back the output

    return output

if __name__ == '__main__':

    main()
