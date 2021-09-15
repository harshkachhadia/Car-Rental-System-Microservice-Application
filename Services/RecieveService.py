
from flask import Flask, make_response,request
import json
import os
import requests
from werkzeug.exceptions import NotFound, ServiceUnavailable


def nice_json(arg):
    resp = make_response(json.dumps(arg, sort_keys=True, indent=4))
    resp.headers['Content-Type']="application/text"
    return resp

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    ''' Greet the user '''
  
    return "Hey! Payment service is up!!"

@app.route('/payment', methods=['POST'])
def payment():
    ''' Get Data from Issue Service '''
    paymentdata = request.form 
    ''' This data will be in JSON Format and wil be stored in paymentdata variable'''
    return nice_json("data recieved")

if __name__ == '__main__':
    app.run(port=5002, debug=True)