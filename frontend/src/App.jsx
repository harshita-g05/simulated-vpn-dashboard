import './App.css'
import { useState, useEffect } from 'react';

function App() {
  const [vpnStatus, setVpnStatus] = useState("Disconnected");
  const [location, setLocation] = useState(null);
  const [ip, setIp] = useState(null);
  const [isLoading, setIsLoading] = useState(null);
  const [isEncrypted, setIsEncrypted] = useState(false);
  const [justConnected, setJustConnected] = useState(false);

  // Check connection status periodically
  useEffect(() => {
    if (vpnStatus === "Connected") {
      const interval = setInterval(async () => {
        try {
          const response = await fetch("http://localhost:5000/status");
          const data = await response.json();
          if (data.status === "Disconnected") {
            setVpnStatus("Disconnected");
            setLocation(null);
            setIp(null);
            setIsEncrypted(false);
          }
        } catch (error) {
          console.error("Status check failed:", error);
        }
      }, 5000);
      
      return () => clearInterval(interval);
    }
  }, [vpnStatus]);

  const handleConnect = async () => {
    try {
      let response;
      if (vpnStatus === "Disconnected") {
        setIsLoading("Connecting");
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        response = await fetch("http://localhost:5000/connect", {
          method: "POST",
        });

        const data = await response.json();
        
        if (data.status === "Connected") {
          setVpnStatus(data.status);
          setLocation(data.location);
          setIp(data.ip);
          setIsEncrypted(data.encrypted);
          setJustConnected(true);
          
          // Remove bounce animation after it plays
          setTimeout(() => setJustConnected(false), 600);
          
          console.log("Server response:", data.server_response);
        } else {
          alert("Connection failed: " + data.error);
        }
        setIsLoading(null);

      } else {
        setIsLoading("Disconnecting");
        await new Promise(resolve => setTimeout(resolve, 500));
        
        response = await fetch("http://localhost:5000/disconnect", {
          method: "POST",
        });
        
        const data = await response.json();
        setVpnStatus(data.status);
        setLocation(null);
        setIp(null);
        setIsEncrypted(false);
        setIsLoading(null);
      }

    } catch (error) {
      console.error("Error connecting to VPN:", error);
      alert("Connection error - make sure the VPN server is running!");
      setIsLoading(null);
    }
  };

  return (
    <div className="dashboard">
      <h1 className="title">VPN Dashboard</h1>
      
      <div className="main-content">
        {/* Left side - Computer character */}
        <div className="computer-section">
          <button 
            className="connect-button" 
            onClick={handleConnect} 
            disabled={isLoading}
          >
            {isLoading ? `${isLoading}...` : vpnStatus === "Connected" ? "Click to Disconnect" : "Click to Connect"}
          </button>
          
          <div className={`computer-container ${justConnected ? 'bounce' : ''}`}>
            <div className="computer-character">
              {vpnStatus === "Connected" ? (
                <img 
                  src="/src/assets/computer-happy.png" 
                  alt="Happy Computer"
                  className="computer-image"
                />
              ) : (
                <img 
                  src="/src/assets/computer-neutral.png" 
                  alt="Neutral Computer"
                  className="computer-image"
                />
              )}
            </div>
          </div>
          
          {isLoading && <div className="loading-text">{isLoading}...</div>}
        </div>

        {/* Right side - Speech bubble (hidden when disconnected) */}
        {vpnStatus === "Connected" && (
          <div className="speech-bubble">
            <h3 className="bubble-title">Connected</h3>
            <div className="info-item">
              <span className="label">Location:</span>
              <span className="value">{location}</span>
            </div>
            <div className="info-item">
              <span className="label">IP Address:</span>
              <span className="value">{ip}</span>
            </div>
            <div className="info-item">
              <span className="label">Encryption: </span>
              <span className="value">
                {isEncrypted ? " Active (Fernet AES-128)" : "✗ None"}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
