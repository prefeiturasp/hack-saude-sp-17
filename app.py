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


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    # res = processRequest(req)
    res = handleRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    print("Response:")
    print(res)

    return r


def handleRequest(req):
    """
    Maps actions requested from api.ai to backend functions.
    """
    action = req.get("result").get("action")

    # constant map of api.ai actions to functions
    action_map = {
        # "medicamento_local": getNearestMedPosition,
        "medicamento_prescritor_sus": canGetMed
    }

    # gets function from action map dictionary
    func = action_map.get(action)

    # executes function
    return func(req)


def canGetMed(req):
    # loads medications to know if they can be retrieved
    with open('medications.json') as medications_file:
        data = json.load(medications_file)

    requested_med = req.get("result").get("parameters").get("nome_medicamento")

    can_get = True
    response_text, output_context = ("", "")

    try:
        can_get = not [med.isAntibiotic for med in data["medications"]
                       if med.name == requested_med]
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
        "contextOut": [{
            "name": output_context,
            "lifespan": 2}],
        "source": "hack-saude-sp-17"
    }

    return response_object


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
