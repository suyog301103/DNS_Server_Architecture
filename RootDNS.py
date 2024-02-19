from socket import *
from Common_to_all import *
import json

# Root DNS port
root_DNS_port = 52311
root_serverSocket = socket(AF_INET, SOCK_DGRAM)
root_serverSocket.bind(('', root_DNS_port))

# Each TLD server designated to a unique port
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

while True:
    print("Root DNS - ON\n")
    # receiving query from Local DNS
    local_DNS_message, local_DNS_address = root_serverSocket.recvfrom(16384)
    TLD_string = local_DNS_message.decode()
    # print("@Root DNS, received : ", TLD_string)

    # # PROCESSING.....
    TLD_dict = json.loads(TLD_string)
    TLD = TLD_dict["Questions"]["Name"][-3:]
    print("TLD extracted = ", TLD)
    
    if TLD == 'com' :
        port = TLD_IPs['com']
    
    elif TLD == 'edu' :
        port = TLD_IPs['edu']
    
    else :
        port = TLD_IPs['org']
    # WHAT TO DO IF NONE OF THESE!!!!!!!!!!!!!
    
    # Sending message to next DNS server
    query = DNS_query_format
    root_serverSocket.sendto(local_DNS_message, (All_Servers_IP, port))

    # Receiving response from TLD server
    TLD_response, TLD_address = root_serverSocket.recvfrom(16384)
    print("TLD -> Root : ", TLD_response.decode())

    # Passing on response to Local DNS
    print("Sending message to Local DNS : ", TLD_response.decode())
    root_serverSocket.sendto(TLD_response, local_DNS_address) 