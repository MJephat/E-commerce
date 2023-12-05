import os
import sqlite3, hashlib, os
from flask import Flask
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'udhu3982398dh7'

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'],))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId,))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


@app.route('/')
def root():
    loggedIn,firstName, noOfItems = getLoginDetails()
    with sqlite.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId,name, price, description,image,stock FROM products WHERE productId')
        itemData = cur.fetchall()
        cur.excute('SELECT categoryId, name FROM categories')
        catedoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)
#LOGIN
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId/Password'
            return render_template('login.html', error=error)

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

@app.route("/registerationForm")
def registerationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)