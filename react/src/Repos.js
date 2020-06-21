import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import RepoClient from './clients/RepoClient';
import Modal from 'react-modal';


Modal.setAppElement('#root')

class Repos extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        repos: [],
        errorMessage: null
    };
    this.update()

    this.onDelete = this.onDelete.bind(this)
    this.toggleVisible = this.toggleVisible.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.closeModal = this.closeModal.bind(this)
  }

  update() {
    RepoClient.getRepos()
              .then( (result) => {
        this.setState({...this.state, repos: result})
    });
  }

  toggleVisible(event) {
    if(event.target.type === "text") {
      event.target.type = "password"
    } else {
      event.target.type = "text"
    }
  }

  closeModal() {
    this.setState({...this.state, errorMessage: null})
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(document.forms[0]);

    this.setState({
            ...this.state, 
            errorMessage: `could not add repo "${document.forms[0].repo.value}"`
          });
    fetch('/v1/repos', {
        method: "POST",
        body: data
    }).then((result) => {
        // TODO 404
        if (result.ok) {
          this.update()
          document.forms[0].repo.value = '';
        } else {
          this.setState({
            ...this.state, 
            errorMessage: `could not add repo "${document.forms[0].repo.value}"`
          });
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
    const response = window.confirm(`Deleting '${repoName}'. Are you sure?`)

    if (response) {
      fetch('/v1/repos/' + repoName, {
        method: "DELETE"
      }).then((result) => {
        if (result.ok) {
          this.update()
        } else {
          this.setState({...this.state, errorMessage: "could not add repo"})
        }
      }).catch((result) => {
        // alert("failed")
      })
    }
  }

  render() {
    const {repos, errorMessage} = this.state;
    const showDialog = errorMessage !== null;
    const graphs = [];

    console.log(showDialog)
    return (
    <div>
      <Modal isOpen={showDialog}>
        <h2>Error.</h2>
        <p>{errorMessage}</p>
        <div>
          <button onClick={this.closeModal}>ok</button>
        </div>
      </Modal>
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
              {graphs.map((url) =>
                <li><a href={url}><img src={url} alt="DOT graph" /></a></li>)}
            </ul>
          </li>
        })}
      </ul>
    </div>
    )
  }
}
  
export default Repos;
