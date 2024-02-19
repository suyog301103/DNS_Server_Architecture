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

#TLD SERVER INFO
# This PORT NUMBER IS stored in the dictionary
TLD_IPs = {'com' : 6000, 'edu' : 6001, 'org' : 6002}

# .com TLD port
google_auth_port = 7000

Auth_IPs = {'google' : 7000, 'amazon' : 7001, 'flipkart' : 7002}

# google auth ports

Services_IP = {"drive" : 8000, "youtube" : 8001, "classroom" : 8002}

# Cache structure = [(Name, Address, Type)]
len_cache = 0
cache = []

while True :
    # receiving query from client
    message, clientAddress = local_serverSocket.recvfrom(4096)        # can receive max of 4 KB
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

        # Local DNS server is the client to Root DNS(sending to Root DNS)
        local_serverSocket.sendto(str(query).encode(), (All_Servers_IP, root_DNS_port))

        # Receving response from Root DNS
        root_message, root_address = local_serverSocket.recvfrom(4096).decode()

        TLD_string = root_message.decode()
        TLD_dict = json.loads(TLD_string)
        TLD = TLD_dict["Questions"]["Name"][-1:-4:-1]
        
        if TLD == 'com' :
            port = TLD_IPs['com']
        
        elif TLD == 'edu' :
            port = TLD_IPs['edu']
        
        else :
            port = TLD_IPs['org']

        if(TLD=='com'):
            # Sending response to TLD server
            local_serverSocket.sendto(str(query).encode(), port)

            # Receving response from TLD(.com TLD server in this case)
            com_TLD_message, com_TLD_address = local_serverSocket.recvfrom(4096)

            message = com_TLD_message.decode()

            if 'google' in com_TLD_message.decode() :
                port = Auth_IPs['google']
            
            elif 'amazon' in com_TLD_message.decode() :
                port = Auth_IPs['amazon']
            
            elif 'flipkart' in com_TLD_message.decode() :
                port = Auth_IPs['flipkart']
            
            else :
                pass
            # DO SOMETHING HEREE!!!!!!!!!!!!

            #sending the response to the auth server
            query = DNS_query_format
            local_serverSocket.sendto(com_TLD_message, (All_Servers_IP, port))

            #receiving the response from the auth server
            if 'google' in com_TLD_message.decode() :
                google_TLD_message, google_TLD_address = local_serverSocket.recvfrom(4096)
                message = google_TLD_message.decode()
                
                if ("drive" in google_TLD_message.decode()):
                    port= Services_IP["drive"]
                
                elif ("youtube" in google_TLD_message.decode()) :
                    port= Services_IP["youtube"]
                
                elif ("classroom" in google_TLD_message.decode()) :
                    port= Services_IP["classroom"]

                else :
                    pass

                response = DNS_response_format
                response["Name"] = message["Questions"]["Name"]
                response["Type"] = message["Questions"]["Type"]
                response["Class"] = message["Questions"]["Class"]
                response["Address"] = port

                #sending the response back to the client
                local_serverSocket.sendto(port, clientAddress)

                # Caching the received response
                if (len_cache < 10) :
                    to_cache = (response['Name'], response['Address'], response["Type"])
                    cache.append(to_cache)
                    len_cache += 1
        
        

