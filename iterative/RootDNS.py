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

root_message, root_address = root_serverSocket.recvfrom(4096).decode()
root_string = root_message.decode()
TLD_dict = json.loads(root_string)
TLD = TLD_dict["Questions"]["Name"][-1:-4:-1]

if TLD == 'com' :
    port = TLD_IPs['com']

elif TLD == 'edu' :
    port = TLD_IPs['edu']

else :
    port = TLD_IPs['org']
