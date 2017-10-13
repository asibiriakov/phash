#!/usr/bin/python3

import paramiko, getpass, json, re

with open('addresses.txt', 'r') as f:
    ips = [line for line in f.readlines()]

servers = {
        "59": 0,
        "65": 0,
        "67": 0,
        "68": 0,
        "70": 0,
        "79": 0,
        "80": 0,
        "767": 0,
        "768": 0,
        "769": 0,
        "770": 0,
        "771": 0,
        "772": 0,
        "773": 0,
        "774": 0,
        }

max_buffer = 65535

def clear_buffer(connection):
        if connection.recv_ready():
                return connection.recv(max_buffer)

connection = paramiko.SSHClient()
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connection.connect('10.10.10.100', username = 'admin', password = 'admin', look_for_keys = False, allow_agent = False)
new_connection = connection.invoke_shell()
output = clear_buffer(new_connection)
time.sleep(2)
new_connection.send("\n")
output = clear_buffer(new_connection)

with open('phash_results.txt', 'w') as f:
        for ip in ips:
                new_connection.send("/i/slb/bind\n")
                new_connection.send(ip)
                new_connection.send("255.255.255.255\n")
                new_connection.send("13\n")
                time.sleep(2)
                output = new_connection.recv(max_buffer)
                output = output.decode('ascii')
                counter = re.search("\d{1,3}\r\n\r\n", output)
                counter = counter.group(0)
                for server in servers:
                        if counter.rstrip() == server:
                                servers[server] += 1

        for server in servers:
                f.write('Server id' + str(server) + ' has ' + str( servers[server]) + ' addresses associated\n')
        print('Completed!')
new_connection.close()
