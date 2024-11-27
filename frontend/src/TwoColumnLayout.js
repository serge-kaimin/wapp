import React, { useState } from "react";
import "./TwoColumnLayout.css";

const API_URL = "api";

const TwoColumnLayout = () => {
  const [idInstance, setIdInstance] = useState("");
  const [apiTokenInstance, setApiTokenInstance] = useState("");
  const [to, setTo] = useState("");
  const [message, setMessage] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [output, setOutput] = useState("");

  // Handle getSetting action
  const handleGetSetting = async () => {
    try {
      const response = await fetch(`${API_URL}/settings`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'idInstance': idInstance,
          'apiTokenInstance': apiTokenInstance,
        }
      });
      const data = await response.json();
      setOutput(JSON.stringify(data, null, 2));
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  // Handle getStateInstance action
  const handleGetStateInstance = async () => {
    try {
        const response = await fetch(`${API_URL}/stateinstance`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'idInstance': idInstance,
            'apiTokenInstance': apiTokenInstance
          }
        });
        const data = await response.json();
        setOutput(JSON.stringify(data, null, 2));
      } catch (error) {
        setOutput(`Error: ${error.message}`);
      }
  };

  // Handle sendMessage action via send_message
  const handleSendMessage = async () => {
    try {
        console.log('idInstance', idInstance);
        console.log('apiTokenInstance', apiTokenInstance);
        console.log('to', to);
        console.log('message', message);
      const response = await fetch(`${API_URL}/sendmessage`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'idInstance': idInstance,
            'apiTokenInstance': apiTokenInstance
          },
        body: JSON.stringify({
            chatId: to,
            message: message
        })
      });
      const data = await response.json();
      setOutput(JSON.stringify(data, null, 2));
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  // Handle sendFileByUrl action
  const handleSendFileByUrl = async () => {
    try {
      const response = await fetch(`${API_URL}/sendfilebyurl`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'idInstance': idInstance,
          'apiTokenInstance': apiTokenInstance
        },
        body: JSON.stringify({
          chatId: to,
          urlFile: mediaUrl
        })
      });
      const data = await response.json();
      setOutput(JSON.stringify(data, null, 2));
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  return (
    <div className="container">
      <div className="column left">
        <form>
          <p></p>
          <div>
            <input
              placeholder="idInstance"
              type="text"
              value={idInstance}
              onChange={(e) => setIdInstance(e.target.value)}
            />
          </div>
          <div>
            <input
              placeholder="ApiTokenInstance"
              type="password"
              value={apiTokenInstance}
              onChange={(e) => setApiTokenInstance(e.target.value)}
            />
          </div>
          <p> </p>
          <div>
            <p>
              <button type="button" onClick={handleGetSetting}>
                getSetting
              </button>
            </p>
            <p>
              <button type="button" onClick={handleGetStateInstance}>
                getStateInstance
              </button>
            </p>
          </div>
          <div>
            <input
              type="text"
              placeholder="77771234567"
              maxLength="20"
              value={to}
              onChange={(e) => setTo(e.target.value)}
            />
          </div>
          <div>
          <textarea
              placeholder="Hello, World!"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows="8"
              className="message"
            />
          </div>
          <div>
            <button type="button" onClick={handleSendMessage}>
              sendMessage
            </button>
          </div>
          <div>
            <input
              placeholder="77771234567"
              type="text"
              maxLength="20"
              value={to}
              onChange={(e) => setTo(e.target.value)}
            />
          </div>
          <div>
            <input
              type="url"
              placeholder="https://my.site.com/img/horse.png"
              value={mediaUrl}
              onChange={(e) => setMediaUrl(e.target.value)}
            />
          </div>
          <div>
            <button type="button" onClick={handleSendFileByUrl}>
              sendFileByUrl
            </button>
          </div>
        </form>
      </div>
      <div className="column right">
        <h2>Response:</h2>
        <textarea
          value={output}
          onChange={(e) => setOutput(e.target.value)}
          className="output"
        />
      </div>
    </div>
  );
};

export default TwoColumnLayout;
