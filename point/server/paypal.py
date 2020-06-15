import logging
from flask import Blueprint, request
from point.models import GitHubUser

LOG = logging.getLogger(__name__)


class PayPalEvent:
    def __init__(self, **attrs):
        self.id = attrs.get('id')
        self.summary = attrs.get('summary')
        self.create_time = attrs.get('create_time')
        self.resource_type = attrs.get('resource_type')
        self.event_type = attrs.get('event_type')
        self.email = attrs.get('resource', {})\
                          .get('subscriber', {})\
                          .get('email_address')
        self.amount = attrs.get('resource',{}).get('amount', {}).get('total')

    def __str__(self):
        return f"<PayPalEvent {self.email} {self.amount}, {self.summary} {self.id}"

paypal_routes = Blueprint('paypal_routes', __name__)


@paypal_routes.route('/paypal/events', methods=["POST"])
def paypal_event():
    LOG.info(f"Incoming PayPal Event: {request.get_json()}")
    event = PayPalEvent(**request.get_json(force=True))
    LOG.debug(event)
    user = GitHubUser.find(email=event.email)
    if user:
        user.balance += event.amount
        if GitHubUser.update(user):
        # if GitHubUser.update(user, balance=user.balance + event.amount):
            LOG.debug("Paypal update succeeded")
            return {"message": "OK"}, 200

    return '{"message": "unknown error"}', 500
