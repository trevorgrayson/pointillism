import React, { Component } from 'react';

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

                <h3>Log Out</h3>
                <a href="/github/logout">logout</a>
            </div>
        )
    }
}

export default Account;
