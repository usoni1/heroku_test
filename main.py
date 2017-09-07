import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGOHQ_URL')
client = MongoClient(MONGO_URL)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
db = client.app76102553
users_collection = db.users
starred_collection = db.user_starred
time_spent_per_page_collection = db.time_spent_per_page
user_vote_collection = db.user_vote
user_bookmarked_collection = db.user_bookmarked
answer_time_spent_collection = db.answer_time_spent

@app.route("/", methods=['GET'])
def index():
    if(session.get("username", False)):
        return redirect("/logged_in")
    return render_template('index.html', sign_up_success = session.get('sign_up_success', False), login_failure = session.get('login_failure', False))

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.form.get('action', None) == 'signup':
            user_data = {"username" : request.form.get('username', None), "password" : request.form.get('password', None)}
            users_collection.insert(user_data)
            session["sign_up_success"] = True
            return redirect('/')
        elif request.form.get('action', None) == 'login':
            cursor = users_collection.find({"username" : request.form.get('username', None), "password" : request.form.get('password', None)})
            if cursor.count() == 1:
                session["username"] = request.form.get('username', None)
                return redirect('/logged_in')
            else:
                session["sign_up_success"] = False
                session["login_failure"] = True
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
    data["username"] = session.get('username', None)
    starred_collection.insert(data)
    return redirect('/')

@app.route("/url_time_spent", methods=['GET', 'POST'])
def url_time_spent():
    data = request.get_json()
    data["username"] = session.get('username', None)
    time_spent_per_page_collection.insert(data)
    return redirect('/')

@app.route("/user_vote", methods=['GET', 'POST'])
def user_vote():
    data = request.get_json()
    data["username"] = session.get('username', None)
    user_vote_collection.insert(data)
    return redirect('/')

@app.route("/user_bookmarked", methods = ['GET', 'POST'])
def user_bookmarked():
    data = request.get_json()
    data["username"] = session.get('username', None)
    user_bookmarked_collection.insert(data)
    return redirect('/')

@app.route("/answer_time_spent", methods = ['GET', 'POST'])
def answer_time_spent():
    data = request.get_json()
    data["username"] = session.get('username', None)
    answer_time_spent_collection.insert(data)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
