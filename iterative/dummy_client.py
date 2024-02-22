from socket import *
from Common_to_all import *

client_port = 52
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind(('', client_port))

local_DNS_port = 53

while True : 
    client_query = input("Enter query : ")
    client_socket.sendto(client_query.encode(), (All_Servers_IP, local_DNS_port))

    #receive from the local DNS
    local_DNS_message, local_DNS_address = client_socket.recvfrom(16384)
    message = local_DNS_message.decode()
    print("the message received from the local dns is: ",message)
