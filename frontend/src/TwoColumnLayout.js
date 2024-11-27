import React, { useState } from 'react';
import './TwoColumnLayout.css';

const TwoColumnLayout = () => {
  const [idInstance, setIdInstance] = useState('');
  const [apiTokenInstance, setApiTokenInstance] = useState('');
  const [to, setTo] = useState('');
  const [message, setMessage] = useState('');
  const [mediaUrl, setMediaUrl] = useState('');
  const [output, setOutput] = useState('');

  const handleGetSetting = () => {
    // Handle getSetting action
  };

  const handleGetStateInstance = () => {
    // Handle getStateInstance action
  };

  const handleSendMessage = () => {
    // Handle sendMessage action
  };

  const handleSendFileByUrl = () => {
    // Handle sendFileByUrl action
  };

  return (
    <div className="container">
      <div className="column left">
        <h2></h2>
        <form>
          <div>
            <label>idInstance:</label>
            <input
              type="text"
              value={idInstance}
              onChange={(e) => setIdInstance(e.target.value)}
            />
          </div>
          <div>
            <label>ApiTokenInstance:</label>
            <input
              type="password"
              value={apiTokenInstance}
              onChange={(e) => setApiTokenInstance(e.target.value)}
            />
          </div>
          <div>
            <p>
            <button type="button" onClick={handleGetSetting}>getSetting</button>
            </p>
            <p>
            <button type="button" onClick={handleGetStateInstance}>getStateInstance</button>
            </p>
          </div>
          <div>
            <label>To:</label>
            <input
              type="text"
              maxLength="20"
              value={to}
              onChange={(e) => setTo(e.target.value)}
            />
          </div>
          <div>
            <label>Message:</label>
            <input
              type="text"
              maxLength="100"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>
          <div>
            <button type="button" onClick={handleSendMessage}>sendMessage</button>
          </div>
          <div>
            <label>To:</label>
            <input
              type="text"
              maxLength="20"
              value={to}
              onChange={(e) => setTo(e.target.value)}
            />
          </div>
          <div>
            <label>Media URL:</label>
            <input
              type="url"
              value={mediaUrl}
              onChange={(e) => setMediaUrl(e.target.value)}
            />
          </div>
          <div>
            <button type="button" onClick={handleSendFileByUrl}>sendFileByUrl</button>
          </div>
        </form>
      </div>
      <div className="column right">
        <h2>Response</h2>
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