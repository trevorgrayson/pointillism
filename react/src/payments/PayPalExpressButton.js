import React from 'react';
import scriptLoader from 'react-async-script-loader';

class PaypalButton extends React.Component {
  constructor(props) {
    super();
    this.state = {
      'host': props.host,
      'buttonId': props.buttonId
    }   
  }

  componentWillReceiveProps ({ isScriptLoaded, isScriptLoadSucceed }) {
    if (isScriptLoaded && !this.props.isScriptLoaded) {
      if (isScriptLoadSucceed) {
        window.paypal.Buttons({
          style: {
              shape: 'rect',
              color: 'blue',
              layout: 'horizontal',
              label: 'paypal',

          },
          createOrder: function(data, actions) {
              return actions.order.create({
                  purchase_units: [{
                      amount: {
                          value: '5'
                      }
                  }],
                  application_context: {
                      shipping_preference: "NO_SHIPPING"
                  }
              });
          },
          onApprove: function(data, actions) {
              return actions.order.capture().then(function(details) {
                  alert('Thank you for your support, ' + details.payer.name.given_name + '!');
              });
          }
        }).render('#paypal-button-container');
      }
      else this.props.onError()
    }
  }

  render() {
    return <form action={`https://${this.state.host}/cgi-bin/webscr`} method="post" target="_top">
      <input type="hidden" name="cmd" value="_s-xclick" />
      <input type="hidden" name="hosted_button_id" value={this.state.buttonId} />
      <table>
      <tr><td><input type="hidden" name="on0" value="Payment Options" />Payment Options</td></tr><tr><td><select name="os0">
        <option value="Appreciation!">Appreciation! : $5.00 USD - monthly</option>
        <option value="Thank you.">Thank you. : $1.00 USD - monthly</option>
        <option value="Sincere Gratitude.">Sincere Gratitude. : $9.00 USD - monthly</option>
      </select> </td></tr>
      </table>
      <input type="hidden" name="currency_code" value="USD" />
      <input type="image" src={`https://${this.state.host}/en_US/i/btn/btn_subscribeCC_LG.gif`} border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" />
      <img alt="" border="0" src={`https://${this.state.host}/en_US/i/scr/pixel.gif`} width="1" height="1" />
    </form>
    
  }
}

export default scriptLoader('https://www.paypalobjects.com/api/checkout.js')(PaypalButton);
