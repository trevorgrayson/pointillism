import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

ReactDOM.render(
  <App host={document.HOST} domain={document.DOMAIN} paypalId={document.PAYPALID} />,
  document.getElementById('root')
);
