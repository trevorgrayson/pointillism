import React from 'react';

function PayPalConfirm(props) {
    const state = props.history.location.state;
    var thankYou = "Thank you for your support";
    if(state.name) {
        thankYou += `, ${state.name}` 
    }
    thankYou += "! You should be expecting an email from PayPal confirming your purchase.";
    
    const item = {name: 'One Time Payment', amount: '$5.00'}

    return (
        <div className="paid">
            <h3>Payment Confirmed.</h3>
            <p>{thankYou}</p>
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr className="dark">
                        <td>{item.name}</td>
                        <td>{item.amount}</td>
                    </tr>
                </tbody>
                
                
            </table>
            <p>
            We hope you enjoy getting started with pointillism.io.  
            Visit <a href="/getting-started">Getting Started</a> for help setting up.
            </p>
            <p>Please <a href="mailto:trevor@ipsumllc.com?subject=Pointillism%20Payment">contact us</a> if 
            you have any questions.</p>
        </div>
    )
}

export default PayPalConfirm;