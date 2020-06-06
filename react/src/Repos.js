import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import RepoClient from './clients/RepoClient';


class Repos extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        repos: []
    };
    this.update()

    this.onDelete = this.onDelete.bind(this)
    this.toggleVisible = this.toggleVisible.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  update() {
    RepoClient.getRepos()
              .then( (result) => {
        this.setState({repos: result})
    });
  }

  toggleVisible(event) {
    if(event.target.type === "text") {
      event.target.type = "password"
    } else {
      event.target.type = "text"
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(document.forms[0]);

    fetch('/v1/repos', {
        method: "POST",
        body: data
    }).then((result) => {
        // TODO 404
        if (result.ok) {
          this.update()
          document.forms[0].repo.value = '';
        } else {
          alert("could not add repo");
        }
    }).catch((result) => {
        // alert("FAILED! " + result)
    });
  }

  keyPressed(event) {
    if(event.key === "Enter") {
      this.handleSubmit(event);
    }
  }

  onDelete(event) {
    const repoName = event //hack
    const response = window.confirm("Deleting '"+repoName+"'. Are you sure?")

    if (response) {
      fetch('/v1/repos/' + repoName, {
        method: "DELETE"
      }).then((result) => {
        if (result.ok) {
          this.update()
        } else {
          window.alert("could not add repo")
        }
      }).catch((result) => {
        // alert("failed")
      })
    }
  }

  render() {
    const {repos} = this.state;

    return (
    <div>
      <form className="repo">
        <h2>Authorize New Repo</h2>
        <TextField name="repo" label="Authorize Repository"
            onKeyPress={(event) => this.keyPressed(event)} />
        <Button variant="contained" color="primary"
            className="repo-submit"
            onClick={this.handleSubmit}>Authorize</Button>
      </form>
      <h2>Authorized Repos ({repos.length})</h2>
      <ul className="repos">
        {repos.map((repo, index) => {
          return <li key={index}>
            <span>{repo.name}</span>
            <input type="password" value={repo.token} onClick={this.toggleVisible} />
            <Button color="secondary" onClick={() => this.onDelete(repo.name)}>Delete</Button>
            <ul className="graphs">
              {repo.graphs.map((graph) =>
                <li><a href={graph.url}><img src={`${graph.url}?token=${repo.token}`} alt="DOT graph" /></a></li>)}
            </ul>
          </li>
        })}
      </ul>
    </div>
    )
  }
}
  
export default Repos;
