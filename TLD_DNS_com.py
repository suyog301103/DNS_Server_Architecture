from socket import *
from Common_to_all import *
import json

# .com TLD port
com_DNS_port = 6000
com_server_socket = socket(AF_INET, SOCK_DGRAM)
com_server_socket.bind(('', com_DNS_port))

Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002}

while True :
    print(".com TLD - ON\n")

    # Receiving message from Root DNS
    root_DNS_message, root_DNS_address = com_server_socket.recvfrom(16384)

    # # PROCESSING..........
    root_DNS_message = json.loads(root_DNS_message.decode())        # brought down to dict form
    print(root_DNS_message)
    
    if 'google' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['google']
    
    elif 'amazon' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['amazon']
    
    elif 'flipkart' in root_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['flipkart']
    
    else :
        pass
    #     # DO SOMETHING HEREE!!!!!!!!!!!!

    # Sending request to Auth
    query = DNS_query_format
    com_server_socket.sendto(json.dumps(root_DNS_message).encode(), (All_Servers_IP, port))

    # Response received here...........
    auth_response, authAddress = com_server_socket.recvfrom(16384)

    #Sending response to Root server here..
    print("Auth -> TLD : ", auth_response.decode())
    com_server_socket.sendto(auth_response, root_DNS_address)