from firebase import firebase
from flask import Flask, jsonify, make_response,request,render_template
import json
import os
import requests
from werkzeug.exceptions import NotFound, ServiceUnavailable
from datetime import date

app = Flask(__name__)

global data
data =  {   "CarID" :  "GJ0000004",
			"CustID" : 121,
			"CustName" : "HastiB",
			"EmailID" : "hasti@gmail.com",
			"ContactNo" : 9997778880,
			"CarName"  : "Hynudai Verna",
            "CarType" : "Sedan",
			"CarColour" : "White",
			"InitialDeposit" : 8000,
			"RatePerKm" : 15,
		}		

@app.route("/")
def hello():
    ''' Greet the user '''
  
    return "Hey! Test Service is up"


@app.route('/issue_call')
def issue_call():

    try:
        req = requests.post("http://127.0.0.1:5001/catalogue2issue/",data)
    except requests.exceptions.ConnectionError:
        return "Services Unavailable"
    return req.text


if __name__ == '__main__':
    app.run(port=5000, debug=True)