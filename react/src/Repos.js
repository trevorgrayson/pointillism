import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import RepoClient from './clients/RepoClient';

class RepoForm extends React.Component {
  constructor(props) {
   super(props);
   this.setState(props)
   this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(document.forms[0]);

    fetch('/v1/repos', {
        method: "POST",
        body: data
    }).then((result) => {
        // TODO 404
        alert("OK")
    }).catch((result) => {
        alert("FAILED! " + result)
    });
  }

  render() {
    return (
      <form className="repo">
        <h2>Authorize New Repo</h2>
        <TextField name="repo" label="Authorize Repository" />
        <Button variant="contained" color="primary" onClick={this.handleSubmit}>Authorize</Button>
      </form>
    )
  }
}

class Repos extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        repos: [
          {"name": "trevorgrayson/privito", "token": "123token"}
        ]
    };
    RepoClient.getRepos()
              .then( (result) => {
        this.setState({repos: result})
    });

    this.onDelete = this.onDelete.bind(this)
    this.toggleVisible = this.toggleVisible.bind(this)
  }

  toggleVisible(event) {
    if(event.target.type === "text") {
      event.target.type = "password"
    } else {
      event.target.type = "text"
    }
  }

  onDelete(event) {
    const repoName = event //hack
    const response = confirm("Deleting '"+repoName+"'. Are you sure?")

    if (response) {
      fetch('/v1/repos/' + repoName, {
        method: "DELETE"
      }).then((result) => {
        alert("OK")
      }).catch((result) => {
        alert("failed")
      })
    }
  }

  render() {
    const {repos} = this.state;

    return (
    <div>
      <RepoForm/>
      <h2>Authorized Repos ({repos.length})</h2>
      <ul className="repos">
        {repos.map((value, index) => {
          return <li key={index}>
            <span>{value.name}</span>
            <input type="password" value={value.token} onClick={this.toggleVisible} />
            <Button color="secondary" onClick={() => this.onDelete(value.name)}>Delete</Button>
          </li>
        })}
      </ul>
    </div>
    )
  }
}
  
export default Repos;
