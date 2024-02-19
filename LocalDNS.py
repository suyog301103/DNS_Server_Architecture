from socket import *
import random
from Common_to_all import *
import json

# IP ADDRESS FOR WHOLE DNS SYSTEM - THIS COMPUTER
# SHOULD UPDATE EVERY TIME NETWORK IS JOINED NEWLY !!!!!!!!!!!!!!!!!!


# LOCAL DNS INFO
local_DNS_port = 53
local_serverSocket = socket(AF_INET, SOCK_DGRAM)
local_serverSocket.bind(('', local_DNS_port))

# ROOT DNS INFO
root_DNS_port = 52311

# Cache structure = [(Name, Address, Type)]
len_cache = 0
cache = []

while True :
    # receiving query from client
    message, clientAddress = local_serverSocket.recvfrom(16384)        # can receive max of 4 KB
    print("Received request for : ", message.decode(), 'from IP address', clientAddress[0])
    
    flag = 0                   # found in cache
    # 1) Check cache
    for cache_elem in cache : 
        if cache_elem[0] == message.decode() :
            flag = 1
            IP_address = cache_elem[1]
    
    # 2) If not found in cache....
    if flag == 0 :
        # have to query the Root DNS
        query = DNS_query_format
        query["Header"]["Transaction_ID"] = random.randint(1, 10)
        query["Header"]["Flags"] = "some_Flag"
        query["Questions"]["Name"] = message.decode()
        query["Questions"]["Type"] = "A"
        query["Questions"]["Class"] = "IN"

        # Sending message to Root DNS
        # json.dumps() being used to maintain double quotes around the dict keys
        # without double quotes around keys, json.loads() will not work
        local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, root_DNS_port))

        # # Receving response from Root DNS
        root_response, root_DNS_address = local_serverSocket.recvfrom(16384)
        root_response = root_response.decode()
        print("Received response = ", root_response, 'from Root DNS\n')

        # # Caching the received response
        # if (len_cache < 10) :
        #     to_cache = (root_response['Name'], root_response['Address'], root_response["Type"])
        #     cache.append(to_cache)
        #     len_cache += 1
        
        # Sending response to client
        #local_serverSocket.sendto(root_response["Address"], clientAddress)
        local_serverSocket.sendto(root_response.encode(), clientAddress)