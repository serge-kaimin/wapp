import React from 'react';
import './TwoColumnLayout.css';

const TwoColumnLayout = () => {
  return (
    <div className="container">
      <div className="column left">
        <h2>Forms</h2>
        {/* Add your request content here */}
      </div>
      <div className="column right">
        <h2>Response</h2>
        {/* Add your response content here */}
      </div>
    </div>
  );
};

export default TwoColumnLayout;