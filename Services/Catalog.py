from flask import Flask, request
from werkzeug.exceptions import NotFound
import json
from flask import make_response
import sqlite3


app = Flask(__name__)

def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


@app.route("/movies", methods=['GET'])
def movie_record():
    conn = sqlite3.connect('C://sqlite/db/carrentsystem.db')
    data_cursor = conn.execute("SELECT * FROM CATALOGUE_DB WHERE AVAILABILITY == 'true';")
    data_master = {}
    cnt = 0
    for row in data_cursor:
        cnt = cnt+1
        data = {}
        data['CarId'] = row[0]
        data['CarName'] = row[1]
        data['CarType'] = row[2]
        data['CarColor'] = row[3]
        data['Deposite Amount'] = row[4]
        data['Rate per Km'] = row[5]
        data_master['Car '+str(cnt)] = data
    return nice_json(data_master)

@app.route("/movies/<Carid>", methods=['GET'])
def movie_record_id(Carid):
    conn = sqlite3.connect('C://sqlite/db/carrentsystem.db')
    data_cursor = conn.execute("SELECT * FROM CATALOGUE_DB WHERE CARID == "+"'"+Carid+"'"+";")
    data = {}
    for row in data_cursor:
        data['CarId'] = row[0]
        data['CarName'] = row[1]
        data['CarType'] = row[2]
        data['CarColor'] = row[3]
        data['Deposite Amount'] = row[4]
        data['Rate per Km'] = row[5]
    return nice_json(data)

@app.route("/return_DB/", methods=['POST'])
def ret_DB():
    Carid = request.form['carId']
    conn = sqlite3.connect('C://sqlite/db/carrentsystem.db')
    data_cursor = conn.execute("UPDATE CATALOGUE_DB set AVAILABILITY = 'true'  WHERE CARID == "+"'"+Carid+"'"+";")
    conn.commit()
    conn.close()
    return nice_json("successful")

@app.route("/issue_DB/", methods=['POST'])
def issue_DB():
    Carid = request.form['carId']
    conn01 = sqlite3.connect('C://sqlite/db/carrentsystem.db')
    data_cursor01 = conn01.execute("UPDATE CATALOGUE_DB set AVAILABILITY = 'false'  WHERE CARID == "+"'"+Carid+"'"+";")
    conn01.commit()
    conn01.close()
    return nice_json('successful')

if __name__ == "__main__":
    app.run(port=5001, debug=True)

