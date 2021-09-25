from flask import Flask, render_template, request, jsonify, session
from markupsafe import escape
import sqlite3 as sql
import GetDriverLocation

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

@app.route('/login')
def login():
    session['username'] = request.form['username']
    session['password'] = request.form['password']
    usr = session['username']
    psw = session['password']
        
    if usr == "Username" and psw == "Password":
        return render_template('hub.html')
    else :
        msg = "Username or Password are not correct!"
        return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    user = "Not Logged!"
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=user)

@app.route('/')
def home():
    return render_template('login.html')

#------------------------------------------------------------
# the error page
#------------------------------------------------------------
# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("404.html")

#------------------------------------------------------------
@app.route('/share_location')
def share_location():
    
    
    return render_template("buggy.html", buggies=records)

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
