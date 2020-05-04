import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';

function convert(href) {
    try {
        const uri = new URL(href);

        if (uri.hostname === 'pointillism.io') {
            return uri
        }

        uri.hostname = 'pointillism.io'
        uri.pathname = uri.pathname + ".svg"
        return uri
    }
    catch (err) {
        return href;
    }
}

class Calculator extends Component {
    constructor(props) {
        super(props);
        this.state = {url: ''}

        this.paste = this.paste.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    paste(event) {
        const url = convert(event.clipboardData.getData('Text'));
        this.setState({url: url});
    }

    onChange(event) {
        this.setState({url: convert(this.state.url)});
    }

    render() {
        return (
            <form className="ptCalculator">
                <p>Or you can paste your DOT Graph Source URL here and it will convert:</p>
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