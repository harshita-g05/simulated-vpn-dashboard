

# our server needs to do 2 things 
# (1) handle networking
# (2) handle encryption 

import socket
import threading
from cryptography.fernet import Fernet
import json

# Load the same shared encryption key as client
with open("backend/key.key", "rb") as f:
    key = f.read()
fernet = Fernet(key)

connected_clients = {}
client_counter = 0

# handle each client connection in a separate thread
def handle_client(conn, addr, client_id):
    print(f"[+] Client {client_id} connected from {addr}")
    connected_clients[client_id] = {
        "connection": conn,
        "address": addr,
        "authenticated": False
    }
    
    try:
        while True:
            encrypted_msg = conn.recv(4096)
            if not encrypted_msg:
                break
            
            # decrypt and process message
            decrypted_msg = fernet.decrypt(encrypted_msg).decode()
            print(f"[CLIENT {client_id}]: {decrypted_msg}")
            
            # parse JSON commands from client
            try:
                data = json.loads(decrypted_msg)
                
                if data.get("action") == "authenticate":
                    connected_clients[client_id]["authenticated"] = True
                    response = json.dumps({
                        "status": "authenticated",
                        "client_id": client_id,
                        "location": data.get("location", "USA 🇺🇸"),
                        "ip": data.get("ip", "8.8.8.8")
                    })
                    encrypted_response = fernet.encrypt(response.encode())
                    conn.send(encrypted_response)
                
                elif data.get("action") == "ping":
                    response = json.dumps({"status": "alive"})
                    encrypted_response = fernet.encrypt(response.encode())
                    conn.send(encrypted_response)
                    
            except json.JSONDecodeError:
                # handle non-JSON messages
                response = f"Echo: {decrypted_msg}"
                conn.send(fernet.encrypt(response.encode()))
                
    except Exception as e:
        print(f"[-] Error with client {client_id}: {e}")
    finally:
        print(f"[-] Client {client_id} disconnected")
        if client_id in connected_clients:
            del connected_clients[client_id]
        conn.close()

# main server loop
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 8080))
server.listen(5)
print("[*] VPN Server listening on port 8080...")

try:
    while True:
        conn, addr = server.accept()
        client_counter += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_counter))
        thread.daemon = True
        thread.start()
except KeyboardInterrupt:
    print("\n[*] Server shutting down...")
    server.close()