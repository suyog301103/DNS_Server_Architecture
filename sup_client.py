from socket import *
from Common_to_all import *

client_port = 52
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind(('', client_port))

# Client is never always-on, but done here for demo only
while True : 
    client_query = input("Enter query : ")
    client_socket.sendto(client_query.encode(), (All_Servers_IP, 53))
    local_dns_message, local_dns_address = client_socket.recvfrom(16348)
    print("IP address (Port number here) : ", local_dns_message.decode())

