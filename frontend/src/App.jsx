import './App.css'
import { useState } from 'react';



function App() {
  {/* isConnected tracks vpn connection and starts as false
    setIsConnected  updates value and useState sets starting 
    val to false */}
  const [vpnStatus, setVpnStatus] = useState("Disconnected");
  const [location, setLocation] = useState(null);
  const [ip, setIp] = useState(null);
  const [isLoading, setIsLoading] = useState(null);


  const handleConnect = async () => {
    try {
      let response;
      if (vpnStatus == "Disconnected") {
        setIsLoading("Connecting"); 
        await new Promise(resolve => setTimeout(resolve, 2000));
        response = await fetch("http://localhost:5000/connect", {
          method: "POST",
        });
      } else {
          setIsLoading("Disconnecting"); 
          await new Promise(resolve => setTimeout(resolve, 1000));
          response = await fetch("http://localhost:5000/disconnect", {
            method: "POST",
          });
      }
    
      const data = await response.json();
      setVpnStatus(data.status); // Should be "Connected"
      setLocation(data.location);
      setIp(data.ip);
      setIsLoading(null);

    } catch (error) {
      console.error("Error connecting to VPN:", error);
      setIsLoading(null);
    }
  };



  return (
    <div className="dashboard">
      <h1>VPN Dashboard</h1>
      <div className="connect-section">
        <button onClick={handleConnect} disabled={isLoading}>
            {isLoading ? `${isLoading}...` : vpnStatus === "Connected" ? "Disconnect" : "Connect"}
        </button>
        {isLoading && <div className="spinner"></div>}
      </div>
      <h4>Status: {vpnStatus}</h4>
      <p>Location: {location}</p>
      <p>IP Address: {ip}</p>
    </div>
  );
}

export default App;
