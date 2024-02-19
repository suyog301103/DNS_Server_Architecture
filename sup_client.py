from socket import *
from Common_to_all import *

client_port = 52
client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.bind(('', client_port))

client_query = input("Enter query : ")
client_socket.sendto(client_query.encode(), (All_Servers_IP, 53))
