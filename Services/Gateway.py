from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
from firebase import firebase
import json
# import jsonify

app = Flask(__name__)

customer_id = ''

def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response

@app.route('/', methods=['GET'])
def home():
    return render_template('gateway.html')

@app.route('/login', methods=['GET'])
def log():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def sign():
    return render_template('signup.html')

@app.route('/signed_up')
def signed_up():
    return '<h1>You have signed up Successfully</h1><br><br><a href="http://127.0.0.1:5000/login">Go To Login</a>'

@app.route('/loged_in')
def loged_in():
    return render_template('services.html')

@app.route('/Failure')  
def failure():
    return '<h1>Failure Occured</h1>'

@app.route('/register_customer', methods=['POST'])
def add_data():
    name = request.form['Name']
    email = request.form['email']
    password = request.form['password']
    contact = request.form['contact']

    data = {
        'Name':name,
        'Email':email,
        'Password':password,
        'Contact':contact
    }

    database = firebase.FirebaseApplication("https://car-rental-system-8036d.firebaseio.com/", None)
    result = database.patch('/Customer/'+contact, data)
    print(result)
    return redirect(url_for('signed_up'))

@app.route('/login_customer', methods=['POST'])
def check_data():
    contact = request.form['email']
    password = request.form['password']

    database1 = firebase.FirebaseApplication("https://car-rental-system-8036d.firebaseio.com/", None)
    data = database1.get('/Customer/'+contact, None)
    if(password == data['Password']):
        customer_id = contact
        return redirect(url_for('loged_in'))
    else:
        return redirect(url_for('Failure'))

@app.route('/list_of_cars', methods=['GET'])
def movie_list():
    try:
        req = requests.get("http://127.0.0.1:5001/movies")
        print(type(json.loads(req.text)))
    except requests.exceptions.ConnectionError:
        return "Service Unavailable"
    return nice_json(json.loads(req.text))

@app.route('/issue_form', methods=['GET'])
def issue():
    return render_template('issue.html')

@app.route('/issue_call', methods=['POST'])
def issue_call():
    CustId = request.form['CustId']
    CarId = request.form['CarId']
    database = firebase.FirebaseApplication("https://car-rental-system-8036d.firebaseio.com/", None)
    data = database.get('/Customer/'+CustId, None)
    CustName = data['Name']
    EmailId = data['Email']
    ContactNo = data['Contact']

    # CarId = 'GJ01AB1234'
    try:
        req = requests.get("http://127.0.0.1:5001/movies/"+CarId)
    except requests.exceptions.ConnectionError:
        print("Service not available")

    data_cust = json.loads(req.text)

    req_data = {
        "CustID":CustId,
        "CustName":CustName,
        "EmailID":EmailId,
        "ContactNo":ContactNo,
        "CarID":CarId,
        "CarName":data_cust['CarName'],
        "CarType":data_cust['CarType'],
        "CarColour":data_cust['CarColor'],
        "InitialDeposit":data_cust['Deposite Amount'],
        "RatePerKm":data_cust['Rate per Km']
    }

    try:
        req = requests.post("http://192.168.43.195:5001/catalogue2issue/",req_data)
    except requests.exceptions.ConnectionError:
        return "Services Unavailable"

    data = {
        'carId':CarId
    }

    try:
        req = requests.post("http://127.0.0.1:5001/issue_DB/", data)
    except requests.exceptions.ConnectionError:
        return "Catalogue service unavailable"
    return req.text

@app.route('/return_form')
def return_form():
    return render_template('return.html')

@app.route('/return_call', methods=['POST'])
def return_call():
    Car_id = request.form['carid']
    kmused = request.form['totalkmused']

    data = {
        "kmused":kmused,
        "car_id":Car_id
    }
    try:
        req = requests.post("http://192.168.43.179:5003/return/",data)
    except requests.exceptions.ConnectionError:
        return "Services Unavailable"
    
    data_ret = json.loads(req.text)
    carid = data_ret['car_id']

    data = {
        'carId':carid
    }

    try:
        req = requests.post("http://127.0.0.1:5001/return_DB/", data)
    except requests.exceptions.ConnectionError:
        return "Catalogue service unavailable"
    return req.text

if __name__=='__main__':
    app.run(port=5000, debug=True)