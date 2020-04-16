import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';


class About extends Component {
  // COVID-19
  //<p>After working in software for over 15 years it becomes obvious that writing software isn't the key challenge, communication is.</p>
//  <p>trevor has been working in software for over 15 years across start ups, private contracting, and enterprise.</p>
//        <p>Good Communication remains the biggest predictor of project success.</p>
  render() {
    return (
      <Typography align="left" paragraph={true}>
        <p><code>pointillism</code> is a passion product written by <a href="https://trevorgrayson.com" target="trevor">trevor grayson</a>.</p>
        <p>This is built with hopes to be part of a larger effort of software projects adopting "real-time" documentation.
        To enable teams to ship well documented, better code, faster.</p>
      </Typography>
    );
  }
}

export default About;
