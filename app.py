#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import Flask
from flask import request
from flask import make_response

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os


from future.standard_library import install_aliases
install_aliases()

# Flask app should start in global layout
app = Flask(__name__)


# constant map of api.ai actions to functions
action_map = {
    "medicamento_local": getNearestMedPosition,
    "medicamento_prescritor_sus": canGetMed,
}


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    # res = processRequest(req)
    res = handleRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def handleRequest(req):
    """
    Maps actions requested from api.ai to backend functions.
    """
    action = req.get("result").get("action")

    # gets function from action map dictionary
    func = action_map.get(action)

    # executes function
    return func(req)

# Medication Requests


def getNearestMedPosition(req):
    pass


def canGetMed(req):
    # loads medications to know if they can be retrieved
    with open('medications.json') as medications_file:
        data = json.load(medications_file)

    requested_med = req.get("result").get("parameters").get("nome_medicamento")

    can_get = False
    response_text, output_context = ("", "")

    try:
        can_get = data.get(requested_med).get("isAntibiotic")
    except Exception as err:
        pass

    # if the med can be required, continue service
    if can_get:
        response_text = ""
        output_context = "medicamento-uso-continuo"
    # if the med can't be retrieved, end service
    else:
        response_text = "Desculpe, mas antibióticos apenas podem ser retirados \
            quando receitados por médicos do SUS."
        output_context = "medicamento-falha"

    response_object = {
        "speech": response_text,
        "displayText": response_text,
        "contextOut": [output_context],
        "source": "hack-saude-sp-17"
        # "data": data,
    }

    return response_object


# def processRequest(req):
#     if req.get("result").get("action") != "yahooWeatherForecast":
#         return {}
#     baseurl = "https://query.yahooapis.com/v1/public/yql?"
#     yql_query = makeYqlQuery(req)
#     if yql_query is None:
#         return {}
#     yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
#     result = urlopen(yql_url).read()
#     data = json.loads(result)
#     res = makeWebhookResult(data)
#     return res


# def makeYqlQuery(req):
#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None

#     retval = "select * from weather.forecast where woeid in \
#              (select woeid from geo.places(1) where text='" + city + "')"

#     return retval


# def makeWebhookResult(data):
#     query = data.get('query')
#     if query is None:
#         return {}

#     result = query.get('results')
#     if result is None:
#         return {}

#     channel = result.get('channel')
#     if channel is None:
#         return {}

#     item = channel.get('item')
#     location = channel.get('location')
#     units = channel.get('units')
#     if (location is None) or (item is None) or (units is None):
#         return {}

#     condition = item.get('condition')
#     if condition is None:
#         return {}

#     # print(json.dumps(item, indent=4))

#     speech = "Today in " + location.get('city') + ": " + \
#         condition.get('text') + ", the temperature is " + \
#         condition.get('temp') + " " + units.get('temperature')

#     print("Response:")
#     print(speech)

#     return {
#         "speech": speech,
#         "displayText": speech,
#         # "data": data,
#         # "contextOut": [],
#         "source": "apiai-weather-webhook-sample"
#     }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
