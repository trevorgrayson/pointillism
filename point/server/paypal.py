import logging
from flask import Blueprint, redirect, request, make_response
from point.models import GitHubUser

LOG = logging.getLogger(__name__)


class PayPalEvent:
    def __init__(self, **attrs):
        self.id = attrs.get('id')
        self.summary = attrs.get('summary')
        self.create_time = attrs.get('create_time')
        self.resource_type = attrs.get('resource_type')
        self.event_type = attrs.get('event_type')
        self.amount = attrs.get('resource', {}).get('amount', {}).get('total')
        self.email = None
        # self. = attrs.get('resource/amount/currency


paypal_routes = Blueprint('paypal_routes', __name__)


@paypal_routes.route('/paypal/events', methods=["POST"])
def paypal_event():
    LOG.info(f"Incoming PayPal Event: {request.get_json()}")
    event = PayPalEvent(**request.get_json())
    user = GitHubUser.find(email=event.email)
    if user:
        user.amount += event.amount
        if GitHubUser.update(user):
            return '{}', 200

    return '{"message": "unknown error"}', 500
