import os
import time, datetime
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGOHQ_URL')
client = MongoClient(MONGO_URL)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
db = client.app76102553
users_collection = db.production_users
starred_collection = db.production_user_starred
time_spent_per_page_collection = db.production_time_spent_per_page
user_vote_collection = db.production_user_vote
user_bookmarked_collection = db.production_user_bookmarked
answer_time_spent_collection = db.production_answer_time_spent
login_history_collection = db.production_login_history
user_searched_collection = db.production_user_searched

@app.route("/", methods=['GET'])
def index():
    if(session.get("username", False)):
        return redirect("/logged_in")
    return render_template('index.html', sign_up_success = session.get('sign_up_success', False),
                           login_failure = session.get('login_failure', False),
                           logout = session.get('logout', False))

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.form.get('action', None) == 'signup':
            user_data = {"username" : request.form.get('username', None), "password" : request.form.get('password', None)}
            users_collection.insert(user_data)
            session["sign_up_success"] = True
            session["login_failure"] = False
            session["logout"] = False
            return redirect('/')
        elif request.form.get('action', None) == 'login':
            cursor = users_collection.find({"username" : request.form.get('username', None), "password" : request.form.get('password', None)})
            if cursor.count() == 1:
                session["username"] = request.form.get('username', None)
                session["login"] = True
                return redirect('/logged_in')
            else:
                session["sign_up_success"] = False
                session["login_failure"] = True
                session["logout"] = False
                return redirect('/')
        else:
            return redirect('/')
    return redirect('/')

@app.route("/logged_in", methods=['GET'])
def logged_in():
    # starred_collection.find({})
    if(session.get("username", False)):
        if(session.get("login", False)):
            session["login"] = False
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H %M %S')
            data = {"username" : session.get("username", False), "timestamp" : st}
            login_history_collection.insert(data)
        login_logs = login_history_collection.find({"username": session.get("username", False)})
        return render_template('logged_in.html', login_logs = login_logs)
    return redirect('/')

@app.route("/user_logs", methods=['GET', 'POST'])
def user_logs():
    if request.method == 'POST':
        if request.form.get('action', None) == "behavioral_logs":
            starred_collection_result = starred_collection.find({"username": session.get("username", False)})
            user_vote_collection_result = user_vote_collection.find({"username": session.get("username", False)})
            user_bookmarked_collection_result = user_bookmarked_collection.find({"username": session.get("username", False)})
            time_spent_per_page_collection_result = time_spent_per_page_collection.find({"username": session.get("username", False)})
            user_searched_collection_result = user_searched_collection.find({"username": session.get("username", False)})
            answer_time_spent_collection_result = answer_time_spent_collection.find({"username": session.get("username", False)})
            return render_template('user_logs.html', starred_collection_result = starred_collection_result,
                                   user_vote_collection_result = user_vote_collection_result,
                                   user_bookmarked_collection_result = user_bookmarked_collection_result,
                                   time_spent_per_page_collection_result = time_spent_per_page_collection_result,
                                   user_searched_collection_result = user_searched_collection_result,
                                   answer_time_spent_collection_result = answer_time_spent_collection_result
                                   )

@app.route("/log_out", methods=['GET', 'POST'])
def log_out():
    if request.method == 'POST':
        if request.form.get('action', None) == "logout":
            session["sign_up_success"] = False
            session["login_failure"] = False
            session["username"] = None
            session["logout"] = True
            return redirect('/')


@app.route("/user_star", methods=['GET', 'POST'])
def starred():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        starred_collection.insert(data)
    return redirect('/')

@app.route("/url_time_spent", methods=['GET', 'POST'])
def url_time_spent():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        time_spent_per_page_collection.insert(data)
    return redirect('/')

@app.route("/user_vote", methods=['GET', 'POST'])
def user_vote():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        user_vote_collection.insert(data)
    return redirect('/')

@app.route("/user_bookmarked", methods = ['GET', 'POST'])
def user_bookmarked():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        user_bookmarked_collection.insert(data)
    return redirect('/')

@app.route("/answer_time_spent", methods = ['GET', 'POST'])
def answer_time_spent():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        answer_time_spent_collection.insert(data)
    return redirect('/')

@app.route("/user_searched", methods = ['GET', 'POST'])
def user_searched():
    data = request.get_json()
    data["username"] = session.get('username', None)
    if data["username"] is not None:
        user_searched_collection.insert(data)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
