import React, { Component } from 'react';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Repos from './Repos';
import About from './About';
import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

class App extends Component {
  render() {
    let repos = [
      'trevorgrayson/private',
      'ipsumllc/sup'
    ]

    return (
      <div className="App">
        <div className="App-header">
          <h2>pointillism.</h2>
        </div>
        <Router>
          <div>
            <Tabs>
                <Tab label="Repos" href="/repos"/>
                <Tab label="About" href="/about"/>
                <Tab label="login" href="/github/login"/>
            </Tabs>
            {/* A <Switch> looks through its children <Route>s and
                renders the first one that matches the current URL. */}
            <Switch>
              <Route path="/about">
                <About/>
              </Route>
              <Route path="/repos">
                <Repos repos={repos}/>
              </Route>
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
