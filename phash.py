#!/usr/bin/python3
#Import modules
import paramiko, getpass, json, re, time
#Open a file with a list of addresses to check against phash
with open('addresses.txt', 'r') as f:
    ips = [line for line in f.readlines()]
#Define servers. Keys are ids and values are counters
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
#Set maximum buffer size
max_buffer = 65535
#Define a function for clearing the output buffer
def clear_buffer(connection):
        if connection.recv_ready():
                return connection.recv(max_buffer)

#Create a new instance of SSHClient class from Paramiko 
connection = paramiko.SSHClient()
#Set the policy that the client should use when the SSH server's hostname is not present
#in either the system host keys or the application's keys
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#Open an ssh connection
connection.connect('10.10.10.100', username = 'admin', password = 'admin', look_for_keys = False, allow_agent = False)
#Invoke a new interactive shell from the connection
new_connection = connection.invoke_shell()
#Clear the output buffer
output = clear_buffer(new_connection)
time.sleep(2)
new_connection.send("\n")
output = clear_buffer(new_connection)
#Open a file for writing
with open('phash_results.txt', 'w') as f:
        # Starts the ips from the addresses.txt file
        for ip in ips:
                new_connection.send("/i/slb/bind\n")
                new_connection.send(ip)
                new_connection.send("255.255.255.255\n")
                new_connection.send("13\n")
                time.sleep(2)
                output = new_connection.recv(max_buffer)
                #Output is a binary string so convert it
                output = output.decode('ascii')
                #Search for a real server id
                counter = re.search("\d{1,3}\r\n\r\n", output)
                #Convert value from re format to a regular string
                counter = counter.group(0)
                #Check if a counter equals to a servers id. If so, increase an appropriate dict value by one
                for server in servers:
                        #rstrip here is to remove \r\n from the counter
                        if counter.rstrip() == server:
                                servers[server] += 1
        #Write a result for each id in the file
        for server in servers:
                f.write('Server id' + str(server) + ' has ' + str( servers[server]) + ' addresses associated\n')
        print('Completed!')
#Close the connection
new_connection.close()
