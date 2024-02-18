from socket import *
from Common_to_all import *

# .com TLD port
com_DNS_port = 6000
com_server_socket = socket(AF_INET, SOCK_DGRAM)
com_server_socket.bind(('', com_DNS_port))

Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002}

while True :
    # receiving query from Root DNS
    root_DNS_message, root_DNS_address = com_server_socket.recvfrom(4096)

    if 'google' in root_DNS_message.decode() :
        port = Auth_IPs['google']
    
    elif 'amazon' in root_DNS_message.decode() :
        port = Auth_IPs['amazon']
    
    elif 'flipkart' in root_DNS_message.decode() :
        port = Auth_IPs['flipkart']
    
    else :
        pass
        # DO SOMETHING HEREE!!!!!!!!!!!!

    query = DNS_query_format
    com_server_socket.sendto(root_DNS_message, (All_Servers_IP, port))

    # Response received here...........
    auth_response, authAddress = com_server_socket.recvfrom(4096)

    #Sending response to Root server here..
    com_server_socket.sendto(auth_response, root_DNS_address)