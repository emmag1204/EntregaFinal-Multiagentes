from flask import Flask
from agent import *
import json
import os
from flask import json

app = Flask(__name__)

@app.route("/simulate", methods = ['GET'])
def agentpy_send_car_positions():
    modelo = runModel(5)
    modelo.run()

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = SITE_ROOT + "/test.json"
    
    data = json.load(open(json_url))
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response


@app.route("/test", methods = ['GET'])
def sopenco():
    data = [
        [{
            "name": "Car0",
            "x": 120,
            "y": 110
        }],
        [{
            "name": "Car0",
            "x": 121,
            "y": 111
        },
        {
            "name": "Car1",
            "x": 122,
            "y": 113
        }
	    ]
    ]

    jsonString = json.dumps(data)
    
    # data = json.load(open(json_url))
    response = app.response_class(
        response= jsonString,
        mimetype='application/json'
    )

    return response



if __name__ == '__main__':
    app.run()

