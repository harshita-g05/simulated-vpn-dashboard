# React and Flask are on different ports so we need to allow 
# cross-origin requests.
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from cryptography.fernet import Fernet
import socket
import json


app = Flask(__name__) # creates web app and ask flask to take care of routing, request and responses
CORS(app)  # Allow React to talk to Flask


# Load encryption key
with open("key.key", "rb") as f:
    key = f.read()
fernet = Fernet(key)

# VPN server connection details
VPN_SERVER_HOST = "127.0.0.1"
VPN_SERVER_PORT = 8080

# Available locations
vpn_locations = [
    {"Country": "Germany","flag": "🇩🇪", "ip": "45.128.92.17"},
    {"Country": "India", "flag": "🇮🇳", "ip": "172.217.0.46"},
    {"Country": "Japan", "flag": "🇯🇵", "ip": "103.5.140.1"},
    {"Country": "USA", "flag": "🇺🇸", "ip": "8.8.8.8"}
]

# Store active connection (in production, use session management)
active_connection = None

# This creates a /log endpoint. Whenever we send a message, it adds a 
# timestamp, writes it to vpn_logs.txt, responds with updated status
@app.route('/log', methods=['POST'])
def receive_log():
    data = request.get_json()
    message = data.get('message')
    
    # Add timestamp to the message
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"

    # Save to log file
    with open("backend/vpn_logs.txt", "a") as f:
        f.write(entry)
    
    print(f"Log: {entry.strip()}")
    return jsonify({"status": "Logged"}), 200


@app.route('/connect', methods=['POST']) #registers a route
def connect_vpn():
    global active_connection
    
    try:
        # Select random VPN location
        selected_location = random.choice(vpn_locations)
        
        # Create socket connection to VPN server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((VPN_SERVER_HOST, VPN_SERVER_PORT))
        
        # Send authentication message with encryption
        auth_data = {
            "action": "authenticate",
            "location": f"{selected_location['Country']} {selected_location['flag']}",
            "ip": selected_location['ip']
        }
        encrypted_auth = fernet.encrypt(json.dumps(auth_data).encode())
        client_socket.send(encrypted_auth)
        
        # Receive response
        encrypted_response = client_socket.recv(4096)
        decrypted_response = fernet.decrypt(encrypted_response).decode()
        response_data = json.loads(decrypted_response)
        
        # Store connection
        active_connection = {
            "socket": client_socket,
            "location": selected_location['Country'] + " " + selected_location['flag'],
            "ip": selected_location['ip']
        }
        
        print(f"VPN Connected: {response_data}")
        
        return jsonify({
            'status': 'Connected',
            'location': active_connection['location'],
            'ip': active_connection['ip'],
            'encrypted': True,
            'server_response': response_data
        })
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return jsonify({
            'status': 'Failed',
            'error': str(e)
        }), 500


@app.route('/disconnect', methods=['POST'])
def disconnect_vpn():
    global active_connection
    
    try:
        if active_connection and active_connection['socket']:
            active_connection['socket'].close()
            print("✓ VPN Disconnected")
        
        active_connection = None
        
        return jsonify({
            'status': 'Disconnected',
            'location': None,
            'ip': None
        })
    except Exception as e:
        return jsonify({
            'status': 'Error',
            'error': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Check if VPN connection is still alive"""
    if not active_connection:
        return jsonify({'status': 'Disconnected'})
    
    try:
        # Send ping to verify connection
        ping_data = {"action": "ping"}
        encrypted_ping = fernet.encrypt(json.dumps(ping_data).encode())
        active_connection['socket'].send(encrypted_ping)
        
        # Wait for response (with timeout)
        active_connection['socket'].settimeout(2)
        encrypted_response = active_connection['socket'].recv(4096)
        
        return jsonify({
            'status': 'Connected',
            'location': active_connection['location'],
            'ip': active_connection['ip']
        })
    except:
        return jsonify({'status': 'Disconnected'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)