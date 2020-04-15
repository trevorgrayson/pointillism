import React, { Component } from 'react';
import './App.css';
import TabNav from './tabs'


class App extends Component {
  render() {
    const repos = []

    return (
      <div className="App">
        <div className="App-header">
          <h2>pointillism.</h2>
        </div>
        <TabNav repos={repos} />
      </div>
    );
  }
}

export default App;
