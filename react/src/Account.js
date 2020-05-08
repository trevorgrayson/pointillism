import React, { Component } from 'react';
import Button from '@material-ui/core/Button';


class Account extends Component {
    constructor(props) {
        super(props);
        this.state = props;
    }

    render() {
        const profile = {
            "name": "Trevor"
        }
        return (
            <div className="profile">
                <h2>{profile.name}</h2>

                <h3>status: basic</h3>
                
                <div>
                    <Button href="/github/logout" color="secondary">Log Out</Button>
                </div>
            </div>
        )
    }
}

export default Account;
