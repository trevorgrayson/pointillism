import os
import json

import renderer


HOST = os.environ['HOST']

def render(event, context):
    path = event['pathParameters']['path']

    response = {
        "statusCode": 200,
        "body": renderer.render(HOST, path)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
