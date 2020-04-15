import React, { Component } from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import TabNav from './tabs'


class App extends Component {
  render() {
    const repos = [
      'trevorgrayson/private',
      'ipsumllc/sup'
    ]

    return (
      <div className="App">
        <div className="App-header">
          <h2>pointillism.</h2>
        </div>
        <TabNav/>
      </div>
    );
  }
}

export default App;
