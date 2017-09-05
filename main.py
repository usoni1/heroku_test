import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGOHQ_URL')
client = MongoClient(MONGO_URL)
app = Flask(__name__)
db = client.app76102553
users_collection = db.users

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_data = {"username" : request.form['username'], "password" : request.form['password']}
        users_collection.insert(user_data)
        return redirect('/logged_in')
    else:
        cursor = users_collection.find({"username" : request.form['name'], "password" : request.form['password']})
        if cursor.count == 1:
            return redirect('/logged_in')
    return redirect('/')

@app.route("/logged_in", methods=['GET'])
def logged_in():
    return render_template('logged_in.html')

@app.route("/user_star", methods=['GET', 'POST'])
def starred():
    data = request.get_json()
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
