#192.168.43.195
from firebase import firebase
from flask import Flask, jsonify, make_response,request,render_template
import json
import os
import requests
from werkzeug.exceptions import NotFound, ServiceUnavailable
from datetime import date

def nice_json(arg):
    resp = make_response(json.dumps(arg, sort_keys=True, indent=4))
    resp.headers['Content-Type']="application/text"
    return resp

DateOfIssue = date.today().strftime("%d/%m/%Y")
fb = firebase.FirebaseApplication('https://car-rental-system-1ca6b.firebaseio.com', None)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    ''' Greet the user '''
  
    return "Hey! Issue Service is up"


@app.route('/catalogue2issue/', methods=['POST'])
def catalogue2issue():
    ''' Get Data from Catalogue Service '''
    data = request.form
    fb.put('CarID/', data["CarID"], {'CustID': data["CustID"], 'CustName': data["CustName"], 'ContactNo': data["ContactNo"], 'EmailID': data["EmailID"], 'CarName': data["CarName"], 'CarType': data["CarType"], 'CarColour': data["CarColour"], 'InitialDeposit': data["InitialDeposit"], 'RatePerKm': data["RatePerKm"],'DateOfIssue': DateOfIssue, 'TotalKmUsed': "0", 'DateOfReturn': "0", 'TotalAmount': "0"})
      
    paymentdata = {"CarID":data["CarID"],"CustID":data["CustID"],"RatePerKm":data["RatePerKm"],"InitialAmountStatus":"1"} 
    #paymentdata = {"CarID":"1234","CustID":"456","InitialDepositeStatus":"1","RatePerKm":"45"}
      
    try:
        req = requests.post("http://192.168.43.122:5002/payment",paymentdata)
        return req.text  
    except requests.exceptions.ConnectionError:
        return "Services Unavailable"

if __name__ == '__main__':
    #app.run(port=5001, debug=True)
    app.run(host="0.0.0.0",port=5001, debug=True)    