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

# TLD server info
# Each TLD server designated to a unique port
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

#specific auth server info's
Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002}

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

        #sending the request to the respective TLD server
        if (int(root_response)==TLD_IPs["com"]):
            print("in touch with .com server")
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, TLD_IPs["com"]))

        elif (int(root_response)==TLD_IPs["edu"]):
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, TLD_IPs["edu"]))

        elif (int(root_response)==TLD_IPs["org"]):
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, TLD_IPs["org"]))

        #### HANDLE ALL THE OTHER CASES LATER!! ####

        #receiving the response from the TLD server
        com_TLD_message, com_TLD_address = local_serverSocket.recvfrom(16384)
        com_TLD_message = com_TLD_message.decode()
        print("Received response = ", com_TLD_message, 'from TLD server\n')

        #sending the request to the respective auth servers
        if (int(com_TLD_message) == Auth_IPs["amazon"]):
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, Auth_IPs["amazon"]))

        elif (int(com_TLD_message) == Auth_IPs["flipkart"]):
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, Auth_IPs["flipkart"]))
        
        elif (int(com_TLD_message) == Auth_IPs["google"]):
            print("in touch with google")
            local_serverSocket.sendto(json.dumps(query).encode(), (All_Servers_IP, Auth_IPs["google"]))

        else :
            pass
        ################# HANDLE OTHER SERVICES #######################

        #receiving the response from the Auth server
        auth_response, authAddress = local_serverSocket.recvfrom(16384)
        print("the response received from the auth server is: ",auth_response.decode())

        #sending the received response back to the client
        local_serverSocket.sendto(auth_response, clientAddress)
        

        # # Caching the received response
        # if (len_cache < 10) :
        #     to_cache = (root_response['Name'], root_response['Address'], root_response["Type"])
        #     cache.append(to_cache)
        #     len_cache += 1
        
        # # Sending response to client
        # #local_serverSocket.sendto(root_response["Address"], clientAddress)
        # local_serverSocket.sendto(root_response.encode(), clientAddress)