from socket import *
from Common_to_all import *
import json

# .com TLD port
google_auth_port = 7000
google_server_socket = socket(AF_INET, SOCK_DGRAM)
google_server_socket.bind(('', google_auth_port))


Services_IP = {"drive" : 8000, "youtube" : 8001, "classroom" : 8002}

while True :
    com_TLD_message, com_TLD_address = google_server_socket.recvfrom(16384)
    message = com_TLD_message.decode()
    message = json.loads(message)
    
    if ("drive" in com_TLD_message.decode()):
        port= Services_IP["drive"]
    
    elif ("youtube" in com_TLD_message.decode()) :
        port= Services_IP["youtube"]
    
    elif ("classroom" in com_TLD_message.decode()) :
        port= Services_IP["classroom"]

    else :
        pass
        ################# HANDLE OTHER SERVICES #######################
    
    # Sending response back to the TLD

    response = DNS_response_format
    response["Name"] = message["Questions"]["Name"]
    response["Type"] = message["Questions"]["Type"]
    response["Class"] = message["Questions"]["Class"]
    response["Address"] = port

    google_server_socket.sendto((json.dumps(response)).encode(), com_TLD_address)
