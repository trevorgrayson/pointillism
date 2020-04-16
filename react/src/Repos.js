import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import { FormControl } from '@material-ui/core';
import Button from '@material-ui/core/Button';


class RepoForm extends Component {
  constructor(props) {
   super();
   this.setState(props)
   this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);

    console.log(data)

    fetch('/', {
        method: "POST",
        body: data
    }).then((result) => {
        console.log(result)
    });
  }

  render() {
      return (
        <form className="repo">
          <h2>Authorize New Repo</h2>
          <TextField label="Authorize Repository" />
          <Button variant="contained" color="primary">Authorize</Button>
        </form>
      )
  }
}

function Repos(props) {
  return (
    <div>
      <RepoForm/>
      <h2>Authorized Repos ({props.repos.length})</h2>
      <ul className="repos">
        {props.repos.map((value, index) => {
          return <li key={index}>{value}</li>
        })}
      </ul>
    </div>
  )
}
  
export default Repos;
