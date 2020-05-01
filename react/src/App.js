import React, { Component } from 'react';
import './App.css';
import TabNav from './Navigation'

class App extends Component {
  constructor(props) {
    super();
    this.state = props;
  }
  render() {
    const host = this.state.host;
    const domain = this.state.domain;
    const paypalId = this.state.paypalId;
    const username = this.state.username;
    const repos = []

    return (
      <div className="App">
        <div className="App-header">
          <noticeable-widget access-token="qX3J6cHosUQbZuvYHcQO" project-id="XAM1Z3O9kQY5jxf2vhPF"></noticeable-widget>
          <h2>pointillism.io</h2>
        </div>
        <TabNav host={host} domain={domain} repos={repos} username={username} />
        <div className="footer">
          <a href="/static/privacy.html">Privacy Policy</a>
        </div>
      </div>
    );
  }
}

export default App;
