import React from 'react';


function Footer() {
    return (
        <div className="footer">
            <ul className="legal">
                <li><a href="/static/terms.html">Terms and Conditions</a></li>
                <li><a href="/static/privacy.html">Privacy Policy</a></li>
                <li><a href="/static/do-not-sell.html">Do Not Sell My Personal Information</a></li>
            </ul>
        </div>
    )
}

export default Footer;