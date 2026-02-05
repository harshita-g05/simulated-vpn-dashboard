A full-stack VPN application with encrypted socket communication using Python, Flask, and React.

## Features
- Encrypted communication using Fernet (AES-128)
- Multi-threaded Python socket server
- React frontend with Flask REST API
- Real-time connection monitoring

## Tech Stack
Frontend: React, Vite  
Backend: Flask, Python sockets  
Encryption: Cryptography library (Fernet)

## Setup
1. Clone the repository
2. Generate encryption key - Type this in terminal: `python generate_key.py`
3. Install Python dependencies - Type this in terminal: `pip install flask flask-cors cryptography`
4. Install frontend dependencies - Type this in terminal: `cd frontend && npm install`
5. Run VPN server - Type this in terminal: `python vpn_server.py`
6. Run Flask backend - Type this in terminal: `python backend/flask_app.py`
7. Run frontend - Type this in terminal: `cd frontend && npm run dev`

## Run 
Open `http://localhost:5173` in your browser!
