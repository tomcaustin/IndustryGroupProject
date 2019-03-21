
# import the Flask class from the flask module

from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
from functools import wraps
from database import Database
from flask_sqlalchemy import SQLAlchemy
from user import User
from database import CursorFromConnectionPool

import psycopg2


# create the application object
POSTGRES = {
    'database':'postgres',
    'host':'localhost',
    'user':'postgres',
    'port':'5432',
    'password':'admin'
}
app = Flask(__name__)
app.secret_key = "Phy6s1o1"
app.database= "postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % POSTGRES

db = SQLAlchemy(app)
db.init_app(app)


CONNECTION_POOL = {
    'database': "postgres",
    'host': "localhost",
    'user':"postgres",
    'port':5433,            # 5432 on Ubuntu
    'password':"bu1ldm3istr"
}

dbase = Database.initialise(**CONNECTION_POOL)


# login required decorator


def login_required(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url


@app.route('/')
@login_required
def home():
    with CursorFromConnectionPool() as cursor:
        cursor.execute('SELECT * FROM users')
        posts = [dict(id=row[0], email=row[1], first_name=row[2], last_name=row[3]) for row in cursor.fetchall()]
    return render_template('index.html', post=posts)
    #return render_template('index.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #error = 'Invalid Credentials. Please try again.'
            flash("Please register to access web site...")
            return redirect(url_for('register'))
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    flash("You were logged out.")
    return redirect(url_for('welcome'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #flash("please register to access web site...")
        if request.form['first_name'] == '' or request.form['last_name'] == '' \
                or request.form['email'] == '' or request.form['password'] == '':
            error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('login'))
        else:
            session['registered'] = True
            return redirect(url_for('home'))
    #flash("please register to access web site...")
    return render_template('register.html')
    #return redirect(url_for('login'))


# start the server with the 'run()' method
if __name__ == '__main__':
    #dbase = Database.initialise(**CONNECTION_POOL)
    app.run(debug=True)
    #app.run()
