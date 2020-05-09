import React from 'react';
import scriptLoader from 'react-async-script-loader';

class PaypalButton extends React.Component {
   componentWillReceiveProps ({ isScriptLoaded, isScriptLoadSucceed }) {
    const self = this;
    if (isScriptLoaded && !self.props.isScriptLoaded) {
      if (isScriptLoadSucceed) {
        window.paypal && window.paypal.Buttons && window.paypal.Buttons({
          style: {
              shape: 'rect',
              color: 'blue',
              layout: 'horizontal',
              label: 'paypal',

          },
          createOrder: function(data, actions) {
              return actions.order.create({
                  purchase_units: [{
                      description: "https://pointillism.io",
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
                window.document.location = '/paypal/confirm';
              });
          }
        }).render('#paypal-button-container');
      }
      else this.props.onError()
    }
  }

  render() {
    return <div id="paypal-button-container"></div>
  }
}

export default scriptLoader('https://www.paypalobjects.com/api/checkout.js')(PaypalButton);
