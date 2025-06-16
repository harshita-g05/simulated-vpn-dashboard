import './App.css'
import { useState } from 'react';



function App() {
  {/* isConnected tracks vpn connection and starts as false
    setIsConnected  updates value and useState sets starting 
    val to false */}
  const [vpnStatus, setVpnStatus] = useState("Disconnected");

  const handleConnect = async () => {
    try {
      let response;
      if (vpnStatus == "Disconnected") {
        response = await fetch("http://localhost:5000/connect", {
          method: "POST",
        });
      } else {
          response = await fetch("http://localhost:5000/disconnect", {
            method: "POST",
          });
      }

      const data = await response.json();
      setVpnStatus(data.status); // Should be "Connected"
    } catch (error) {
      console.error("Error connecting to VPN:", error);
    }
  };



  return (
    <div className="dashboard">
      <h1>VPN Dashboard</h1>
      <button onClick={handleConnect}>
        {vpnStatus === "Connected" ? "Disconnect" : "Connect"}
      </button>
      <p>Status: {vpnStatus}</p>
    </div>
  );
}

export default App;
