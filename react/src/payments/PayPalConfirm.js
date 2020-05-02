import React from 'react';

function PayPalConfirm() {
    return (
        <div className="paid">
            <h3>Payment Confirmed.</h3>
            <p>Thank you for your support!</p>
            <table>
                <tr>
                    <th></th>
                    <th>Amount</th>
                </tr>
                <tr>
                    <td>One Time Payment</td>
                    <td>$5.00</td>
                </tr>
            </table>
            <p>
            We hope you enjoy getting started with pointillism.io.
            Please <a href="mailto:trevor@ipsumllc.com?subject=Pointillism%20Payment">contact us</a> if 
            you have any questions.</p>
        </div>
    )
}

export default PayPalConfirm;