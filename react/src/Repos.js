import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';


function RepoForm(props) {
  return (
    <form className="repo">
      <h2>Authorize New Repo</h2>
      <TextField label="Authorize Repository" />
      <Button variant="contained" color="primary">Authorize</Button>
    </form>
  )
}

function Repos(props) {
  return (
    <div>
      <RepoForm/>
      <h2>Authorized Repos ({props.repos.length})</h2>
      <ul class="repos">
        {props.repos.map((value, index) => {
          return <li key={index}>{value}</li>
        })}
      </ul>
    </div>
  )
}
  
export default Repos;
