from socket import *
from Common_to_all import *
import json

# .com TLD port
com_DNS_port = 6000
com_server_socket = socket(AF_INET, SOCK_DGRAM)
com_server_socket.bind(('', com_DNS_port))

Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002}

while True:
    # Receiving message from local DNS server
    local_DNS_message, local_DNS_address = com_server_socket.recvfrom(16384)

    # # PROCESSING..........
    local_DNS_message = json.loads(local_DNS_message.decode())        # brought down to dict form
    print(local_DNS_message)

    if 'google' in local_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['google']

    elif 'amazon' in local_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['amazon']

    elif 'flipkart' in local_DNS_message["Questions"]["Name"] :
        port = Auth_IPs['flipkart']

    else :
        pass
    #     # DO SOMETHING HEREE!!!!!!!!!!!!

    # Sending the response(the port number of the respective auth server) back to the local DNS
    query = DNS_query_format
    print("Sending message to Local DNS : ", port)
    com_server_socket.sendto(str(port).encode(), (local_DNS_address))

    # # Response received here...........
    # auth_response, authAddress = com_server_socket.recvfrom(16384)

    # #Sending response to Root server here..
    # com_server_socket.sendto(auth_response, root_DNS_address)
