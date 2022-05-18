import paramiko
import json

#! /usr/bin/python

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)


ssh.connect()

ssh_stdin, ssh_stdout, stderr = ssh.exec_command("ps aux | awk -v OFS=, '{print $1, $2, $3, $4, $10}' | jq -R 'split(",") | {user: .[0], pid: .[1], CPU: .[2], MEM: .[3], TIME: .[4]}'| jq -ns 'inputs' > datos.json")

print(ssh_stdout.read())

with open('datos.json') as file:
    datos = json.load(file)
    for proceso in datos['procesos']:
        if float(float(proceso['MEM'])) > 4.5:
            ssh_stdin, ssh_stdout, stderr = ssh.exec_command("kill -9 " + proceso['pid'])
        else:
            ssh.close()
