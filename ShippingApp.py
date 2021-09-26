from flask import Flask, render_template, request, jsonify, session, redirect, make_response
from markupsafe import escape
import sqlite3 as sql
import GetDriverLocation

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        usr  = request.form['username']
        psw = request.form['password']
        
        if usr == "Username" and psw == "Password":
            session['username'] = usr
            session['password'] = psw

            return redirect("/hub", code=302)
        else :
            msg = "Username or Password are not correct!"
            return render_template('login.html', msg=msg)
    else:
        if "msg" in session:
            msg=session["msg"]
            session.pop('msg', None)
            return render_template('login.html', msg=msg)
        else:
            return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return redirect("/", code=302)

@app.route('/')
def home():
    return render_template("index.html")

#------------------------------------------------------------
# the error page
#------------------------------------------------------------
# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("404.html")

#------------------------------------------------------------
@app.route('/hub')
def share_location():

    # Check if they actually have a session.
    if ("username" in session ) and ("password" in session):
        GetDriverLocation.getDriverLocation()
        latitude_origin = GetDriverLocation.latitude
        longitude_origin = GetDriverLocation.longitude
        latitude_destination = GetDriverLocation.newLatitude
        longitude_destination = GetDriverLocation.newLongitude

        r = make_response(render_template("hub.html", latitude_origin=latitude_origin, longitude_origin=longitude_origin, latitude_destination=latitude_destination, longitude_destination=longitude_destination))
        r.headers.set("Access-Control-Allow-Origin", "https://maps.googleapis.com/*")

        return r
    else:
        session["msg"] = "You need to be logged in to do that."
        return redirect("/login", code=302)

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
