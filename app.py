import sqlite3
import os
from flask import Flask, request, redirect, url_for, abort, render_template, flash, session, g, escape


# CVs = dict()  # username: table_id
users = dict()  # login: password
users['admin'] = 'default'

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
    with app.open_resource('scheme.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


with app.app_context():
    init_db()


@app.route('/')
def hello_page():
    return render_template("layout.html")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text, login) values (?, ?, ?)',
               [request.form['title'], request.form['text'], session['username']])
    print(request.form['title'], request.form['text'], session['username'])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/')
@app.route('/show_entries')
def show_entries():
    db = get_db()
    # try:
    cur = db.execute(f"select title, text from entries where login='{session['username']}' order by id desc limit 1")
    # except Exception as e:
    #     print(e)
    #     return render_template('show_entries.html')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in users.keys():
            error = 'Invalid username'
        elif request.form['password'] != users[request.form['username']]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash(f'You were logged in, login is {request.form["username"]}')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] in users.keys():
            error = "You can't use this username (username is already taken)"
        else:
            users[request.form['username']] = request.form['password']
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash(f'New account was created, login is {request.form["username"]}')
            return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('hello_page'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
