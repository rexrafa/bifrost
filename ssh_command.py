import paramiko

def connect_ssh(host, user, key,command):
    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key, timeout=2)
        stdin, stdout, stderr = client.exec_command(command)
        stdout = stdout.readlines()
        client.close()
        return stdout
    except Exception as e:
        return None