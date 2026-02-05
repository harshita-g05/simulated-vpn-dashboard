

import socket #load networking module (creates tcp/udp connections)
from cryptography.fernet import Fernet

# Load thr same shared key as server
with open("backend/key.key", "rb") as f:
    key = f.read()
fernet = Fernet(key)

# Connect to the server
host = "127.0.0.1"  #set server ip address to same computer 
port = 8080 


#creating a tcp socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
try:
    print("Attempting to connect to server...")
    client.connect((host, port))
    print("[+] Connected to VPN server")
except Exception as e:
    print("Failed to connect:", e)



# Send/receive loop
while True:
    msg = input("Send to server: ") #get user input 
    encrypted_msg = fernet.encrypt(msg.encode())
    client.send(encrypted_msg) #encrypt and send msg

    encrypted_reply = client.recv(4096) #wait for server response
    print(f"[SERVER]: {fernet.decrypt(encrypted_reply).decode()}") #decrypt server reply

client.close()