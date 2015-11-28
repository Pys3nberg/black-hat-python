import paramiko

def ssh_command(ip, user, password, command):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_sessiion = client.get_transport().open_session()

    if ssh_sessiion.active:
        ssh_sessiion.exec_command(command)
        print(ssh_sessiion.recv(1024))

    return

if __name__ == '__main__':

    ssh_command('192.168.0.25', 'pysenberg', 'f7B$APA8', 'ls')