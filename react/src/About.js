import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import { Link } from "react-router-dom";
import Mailchimp from 'react-mailchimp-form';

class About extends Component {
  // COVID-19
  //<p>After working in software for over 15 years it becomes obvious that writing software isn't the key challenge, communication is.</p>
  //  <p>trevor has been working in software for over 15 years across start ups, private contracting, and enterprise.</p>
  //        <p>Good Communication remains the biggest predictor of project success.</p>
  render() {
    const featureUrl = "https://github.com/trevorgrayson/pointillism/issues/new?assignees=trevorgrayson&labels=enhancement&template=feature_request.md&title=FEAT%3A";
    const bugUrl = "https://github.com/trevorgrayson/pointillism/issues/new?assignees=trevorgrayson&labels=bug&template=bug_report.md&title=BUG%3A+";
  
    return (
      <Typography align="left" paragraph={true}>
        <p><code>pointillism</code> is a passion product written by <a href="https://trevorgrayson.com" target="trevor">trevor grayson</a>.</p>
        <p>This is built with hopes to be part of a larger effort of software projects adopting "real-time" documentation.
        To enable teams to ship well documented, better code, faster.</p>
        <p>We would love to hear your thoughts about <code>pointillism.io</code>.  
        Feel free to <a href={featureUrl}>propose a feature</a>, 
         <a href={bugUrl}>report a bug</a>, or <Link to="https://pointillism.slack.com/get-started#/create">slack us</Link>.</p>

        <fieldset>
          <legend>Contact Us</legend>
          <form action="https://getform.io/f/a61d2701-a856-4e1c-9cc0-106ef214c18f" method="POST">
            <TextField label="your name" name="name" fullWidth={true} /><br/>
            <TextField label="email" name="email" fullWidth={true} /><br/>
            <TextField label="message" name="message" 
              fullWidth={true} 
              multiline={true} 
              rows="5" /><br/>
            <button type="submit">Send</button>
          </form>
        </fieldset>

        <fieldset>
          <legend>Subscribe!!!</legend>

          We'll tell you about new features and relevant content.<br/>
          <span className="subtext">(It's mailchimp, you can unsubscribe.)</span>
          <Mailchimp
          action="https://pointillism.us10.list-manage.com/subscribe/post?u=f62d199b0350ecb5e414106cb&amp;id=e0755fc3ea"
          fields={[
            {
              name: 'EMAIL',
              placeholder: 'Email',
              type: 'email',
              required: true
            }
          ]}
        />
        </fieldset>
      </Typography>
      // message next to be TextArea
    );
  }
}

export default About;
