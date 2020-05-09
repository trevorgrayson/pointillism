import React from 'react';

function PayPalConfirm({name}) {
    var thankYou = "Thank you for your support";
    if(name) {
        thankYou += `, ${name}` 
    }
    thankYou += "! You should be expecting an email from PayPal confirming your purchase.";
    

    return (
        <div className="paid">
            <h3>Payment Confirmed.</h3>
            <p>{thankYou}</p>
            <table>
                <tr>
                    <th></th>
                    <th>Amount</th>
                </tr>
                <tr className="dark">
                    <td>One Time Payment</td>
                    <td>$5.00</td>
                </tr>
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