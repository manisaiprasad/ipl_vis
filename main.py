import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from app import init_dashboard
from batsman import init_batsman
from bowler import init_bowler
app = Flask(__name__)
app.secret_key = "super secret key"

# Firebase Config
config = {
    "apiKey": "AIzaSyDjn5XzFuGjF4n98TxBpr7hJLXKAK4mdlY",
    "authDomain": "ipl-viz.firebaseapp.com",
    "databaseURL": "https://ipl-viz-default-rtdb.firebaseio.com/",
    "storageBucket": "ipl-viz.appspot.com"
}

# initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

dashapp = init_dashboard(app)
batsman = init_batsman(app)
bowler = init_bowler(app)


@app.route('/')
def index():
    if isloggedin():
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/dash')
def home():
    if isNotLoggedin():
        return redirect(url_for('login'))
    data = db.child("users").get()
    session['user_name'] = data.val()[session['user_id']]['name']
    return redirect('/dashboard/')
    # return render_template('home.html', name=name, email=session['email'])


@app.route('/batsmen')
def batsman():
    if isNotLoggedin():
        return redirect(url_for('login'))

    return batsman.index()


@app.route('/bowler')
def bowler():
    if isNotLoggedin():
        return redirect(url_for('login'))

    return bowler.index()


@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    if isloggedin():
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            data = {
                "name": name,
                "email": email
            }
            # user = auth.sign_in_with_email_and_password(email, password)
            db.child("users").child(user['localId']).set(data)
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('signup.html', error=str(e))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if isloggedin():
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            app.secret_key = 'secret123'
            user = auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            flash('Login Failed')
            return render_template('login.html', error=str(e))
        session['user'] = user['idToken']
        session['user_id'] = user['localId']
        print(session['user'])
        session['email'] = email
        data = db.child("users").get()
        user['name'] = data.val()[session['user_id']]['name']

        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


def isloggedin():
    if 'user' in session:
        return True
    return False


def isNotLoggedin():
    if 'user' not in session:
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
