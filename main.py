import os
import sqlite3, hashlib, os
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'udhu3982398dh7'

#register
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as conn:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error ocured"
        con.close()
        return render_template("login.html", error=msg)