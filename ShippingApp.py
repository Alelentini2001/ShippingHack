from flask import Flask, render_template, request, jsonify, session, redirect
from markupsafe import escape
import sqlite3 as sql
import GetDriverLocation

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        session['username'] = request.form['username']
        session['password'] = request.form['password']
        usr = session['username']
        psw = session['password']
        
        if usr == "Username" and psw == "Password":
            return redirect("/hub", code=302)
        else :
            msg = "Username or Password are not correct!"
            return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
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
@app.route('/hub')
def share_location():
    GetDriverLocation.getDriverLocation()
    latitude_origin = GetDriverLocation.latitude
    longitude_origin = GetDriverLocation.longitude
    latitude_destination = GetDriverLocation.newLatitude
    longitude_destination = GetDriverLocation.newLongitude

    return render_template("hub.html", latitude_origin=latitude_origin, longitude_origin=longitude_origin, latitude_destination=latitude_destination, longitude_destination=longitude_destination)

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
