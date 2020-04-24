from flask import Blueprint, redirect, request, make_response

paypal_routes = Blueprint('paypal_routes', __name__)


@paypal_routes.route('/paypal/events')
def paypal_event():
    return 'ok'
