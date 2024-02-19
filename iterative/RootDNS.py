from socket import *
import random
from Common_to_all import *
import json

root_DNS_port = 52311
root_serverSocket = socket(AF_INET, SOCK_DGRAM)
root_serverSocket.bind(('', root_DNS_port))

# Each TLD server designated to a unique port
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

while True:
    #receiveing from the local DNS
    local_DNS_message, local_DNS_address = root_serverSocket.recvfrom(16384)

    # # PROCESSING.....
    root_string = json.loads(local_DNS_message)
    TLD = root_string["Questions"]["Name"][-3:]
    print("TLD extracted = ", TLD)

    if TLD == 'com' :
        port = TLD_IPs['com']

    elif TLD == 'edu' :
        port = TLD_IPs['edu']

    else :
        port = TLD_IPs['org']

    # sending the ip address of the respective TLD server back to the local DNS server
    print("Sending message to Local DNS : ", port)
    root_serverSocket.sendto(str(port).encode(), (local_DNS_address))
