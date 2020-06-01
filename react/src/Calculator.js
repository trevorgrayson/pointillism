import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';

class Calculator extends Component {
    constructor(props) {
        super(props);
        this.state = {url: ''}

        this.paste = this.paste.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    paste(event) {
        this.convert(event.clipboardData.getData('Text'), this);
    }

    onChange(event) {
        this.convert(this.state.url, this);
        // this.setState({url: convert()});
    }

    convert(href, self) {
        try {
            fetch("/convert", {
                method: "post",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                {"url": href}
                ),
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                self.setState({url: data.url});
            });
        }
        catch (err) {
            return href;
        }
    }

    render() {
        return (
            <form className="ptCalculator">
                <h3>Paste your DOT Graph Source URL here and the URL will convert:</h3>
                <TextField 
                    name="url" 
                    value={this.state.url} 
                    label="DOT Graph Source URL"
                    fullWidth="true"
                    onChange={this.onChange}
                    onPaste={this.paste} />
            </form>
        )
    }
}

export default Calculator
