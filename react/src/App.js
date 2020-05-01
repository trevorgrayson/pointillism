import React, { Component } from 'react';
import './App.css';
import TabNav from './Navigation'
import Footer from './layout/Footer'


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
        <TabNav host={host} domain={domain} repos={repos} username={username} paypalId={paypalId} />
        <Footer />
      </div>
    );
  }
}

export default App;
