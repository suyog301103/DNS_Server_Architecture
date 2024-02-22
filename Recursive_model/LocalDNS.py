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

# Cache structure = [{DNS_Response_Format}]
len_cache = 0
cache = []

while True :
    print("Local DNS - ON\n")

    # receiving query from client
    message, clientAddress = local_serverSocket.recvfrom(16384)        # can receive max of 4 KB
    # print("Received request for : ", message.decode(), 'from IP address', clientAddress[0])
    
    flag = 0                   # found in cache
    # 1) Check cache
    for cache_elem in cache : 
        if cache_elem['Name'] == message.decode() :
            flag = 1
            local_serverSocket.sendto((json.dumps(cache_elem)).encode(), clientAddress)
            break
    
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
        root_response = json.loads(root_response.decode()) # dictionary

        # Caching the received response
        if (len_cache < 10) :
            cache.append(root_response)
            len_cache += 1
        
        # Sending response to client
        print("Local DNS server received : ", root_response)
        local_serverSocket.sendto((json.dumps(root_response)).encode(), clientAddress)