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
    const data = new FormData(event.target);

    fetch('/', {
        method: "POST",
        body: data
    }).then((result) => {
//        console.log(result)
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

class Repos extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        repos: []
    };
    (new RepoClient()).getRepos()
                      .then( (result) => {
        this.setState({repos: result})
    });
  }

  render() {
    const {repos} = this.state;

    return (
    <div>
      <RepoForm/>
      <h2>Authorized Repos ({repos.length})</h2>
      <ul className="repos">
        {repos.map((value, index) => {
          return <li key={index}>{value}</li>
        })}
      </ul>
    </div>
    )
  }
}
  
export default Repos;
