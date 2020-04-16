import React, { Component } from 'react';
import './App.css';
import TabNav from './tabs'


class App extends Component {
  constructor(props) {
    super();
    this.state = props;
  }
  render() {
    const host = this.state.host;
    const domain = this.state.domain;
    const paypalId = this.state.paypalId;
    const repos = []

    return (
      <div className="App">
        <div className="App-header">
          <h2>pointillism.io</h2>
        </div>
        <TabNav host={host} domain={domain} repos={repos} />
      </div>
    );
  }
}

export default App;
