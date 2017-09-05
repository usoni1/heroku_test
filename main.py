import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGOHQ_URL')
client = MongoClient(MONGO_URL)
app = Flask(__name__)
db = client.app76102553
users_collection = db.users
starred_collection = db.user_starred

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.form.get('action', None) == 'signup':
            user_data = {"username" : request.form.get('username', None), "password" : request.form.get('password', None)}
            users_collection.insert(user_data)
            return redirect('/')
        elif request.form.get('action', None) == 'login':
            cursor = users_collection.find({"username" : request.form.get('username', None), "password" : request.form.get('password', None)})
            if cursor.count() == 1:
                session["username"] = request.form.get('username', None)
                return redirect('/logged_in')
            else:
                return redirect('/')
        else:
            return redirect('/')
    return redirect('/')

@app.route("/logged_in", methods=['GET'])
def logged_in():
    # starred_collection.find({})
    return render_template('logged_in.html')

@app.route("/user_star", methods=['GET', 'POST'])
def starred():
    data = request.get_json()
    starred_collection.insert(data)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
