from flask import Flask, render_template, request, jsonify, session
from markupsafe import escape
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/login', methods=['GET', 'POST'])
def login():
    what = "Log In"
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        usr = session['username']
        psw = session['password']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT password FROM buggies WHERE username=?", (usr,))
                check_psw = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                print(check_psw.replace("'",""))
                if psw == check_psw.replace("'",""):
                    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=usr)
                else:
                    msg = "Wrong Password"
                    return render_template("updated.html", msg = msg)
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
            msg = "error in update operation"
        finally:
            con.close()
        return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=session['username'])
    return render_template('login.html', what=what)

@app.route('/register', methods=['GET', 'POST'])
def register():
    what = "Register"
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        usr = session['username']
        psw = session['password']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT username FROM buggies")
                check_usr = str(cur.fetchall()).replace(",","").replace("(", "").replace(")","");
                try:
                    if usr not in check_usr:
                        cur.execute("INSERT INTO buggies (username, password) VALUES (?,?)", 
                        (usr, psw)
                        )
                    else:
                        cur.execute(
                        "UPDATE buggies SET username=?, password=?",
                        (usr, psw)
                        )
                except:
                    cur.execute("INSERT INTO buggies (username, password) VALUES (?,?)", 
                    (usr, psw)
                    )
                con.commit()
                msg = "Record successfully saved"
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
            msg = "error in update operation"
        finally:
            con.close()
        return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=session['username'])
    return render_template('login.html', what=what)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    user = "Not Logged!"
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=user)

@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# the error page
#------------------------------------------------------------
# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("404.html")

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        #Something there
    elif request.method == 'POST':
        
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM buggies")
                buggy_id_d = str(cur.fetchall()).replace(",","").replace("(","").replace(")","");
                if buggy_id in buggy_id_d :
                    cur.execute(
                    "UPDATE buggies SET qty_wheels=?, tyres=?, qty_tyres=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, aux_hamster_booster=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, total_cost=? WHERE id=?",
                    (qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost, buggy_id)
                    )
                else:
                    cur.execute("INSERT INTO buggies (id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (buggy_id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost,)
                    )    
                con.commit()
                msg = "Record successfully saved"
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall(); 
    con.close()
    return render_template("buggy.html", buggies=records)

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
