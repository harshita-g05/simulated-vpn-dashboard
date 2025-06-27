# React and Flask are on different ports so we need to allow 
# cross-origin requests.
from flask import Flask, jsonify, request
from flask_cors import CORS
import random


app = Flask(__name__) # creates web app and ask flask to take care of routing, request and responses
CORS(app)  # Allow React to talk to Flask

vpn_locations = [
    {"Country": "Germany","flag": "🇩🇪", "ip": "45.128.92.17"},
    {"Country": "India", "flag": "🇮🇳", "ip": "172.217.0.46"},
    {"Country": "Japan", "flag": "🇯🇵", "ip": "103.5.140.1"},
    {"Country": "USA", "flag": "🇺🇸", "ip": "8.8.8.8"}
]



@app.route('/connect', methods=['POST']) #registers a route
def connect_vpn():
    print("VPN Connect request received")
    fake_vpn = random.choice(vpn_locations)
    return jsonify({'status': 'Connected', 
                    'location': f"{fake_vpn['Country']} {fake_vpn['flag']}",
                    'ip': fake_vpn["ip"] } )

@app.route('/disconnect', methods=['POST'])
def disconnect_vpn():
    print("VPN Disconnect request received")
    return jsonify({'status': 'Disconnected', 
                    'location': None,
                    'ip': None})


if __name__ == '__main__':
    app.run(debug=True)