import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';


class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'github': 'loading...',
            'email': 'loading...'
        }
    }

    componentDidMount() {
        const self = this;

        fetch('/v1/profile')
            .then((response) => response.json())
            .then((response) => {
                self.setState(response)
            }).catch((error) => {
                alert(error)
            })
    }

    render() {
        return (<div>
            <h2>Profile</h2>
            <TextField name="github_name" 
                      label="GitHub Account" 
                      value={this.state.github_name} /><br/>
            <TextField name="email" 
                      label="PayPal Email" 
                      value={this.state.email || ''} />
            
            <h2>Logout</h2>
            <Button color="secondary" href="/github/logout">logout</Button>            
        </div>);
    }
}

export default Profile;