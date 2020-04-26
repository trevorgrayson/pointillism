import React from 'react';

class Account extends React.Component {
    render() {
        const unsubscribeUrl = 'https://www.paypal.com/cgi-bin/webscr?cmd=_subscr-find&alias=SGGGX43FAKKXN&switch_classic=true';

        return <div>
            <a href={this.unsubscribeUrl}>
                <img src="https://www.paypalobjects.com/en_US/i/btn/btn_unsubscribe_LG.gif" />
            </a>
        </div>
    }
}