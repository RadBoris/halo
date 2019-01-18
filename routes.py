from flask import Flask, render_template, request, session, redirect, url_for
from models import User, Info
from forms import SignupForm, LoginForm, InfoForm, SearchForm
from database import db_session
from sqlalchemy import and_, or_, not_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =" postgres://ubzdjahonslgwk:4516f846862bbb569079f2b53bcccd8a145315c17098df6390746eee91fd9995@ec2-184-72-230-93.compute-1.amazonaws.com:5432/daco986o48khus"

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about", methods=["GET", "POST"])
def about():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = SearchForm()
  cid = session['id']
  email = session['email']
  user = User.query.filter_by(email=email).first()
  keys = Info.query
  results = []
  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      if form.search.data is not None:
        results = db_session.query(Info).filter(Info.key.like('%' + form.search.data + '%'), Info.user_id==cid)
        return render_template('results.html', results=results)

  elif request.method == "GET":
    return render_template('about.html', form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db_session.add(newuser)
      db_session.commit()
      session['id'] = newuser.uid
      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))
  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data
      password = form.password.data
      user = db_session.query(User).filter(User.email==email).first()
      if user is not None and user.check_password(password):
        session['email'] = user.email
        session['id'] = user.uid
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))
  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))
  email = session['email']
  form = InfoForm()
  key = ''
  value= ''

  user = db_session.query(User).filter(User.email==email).first()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('home.html', form=form)
    else:

      key = form.key.data
      value = form.value.data
      newinfo = Info(form.key.data, form.value.data, user.uid)
      db_session.add(newinfo)
      db_session.commit()

      return render_template('home.html', form=form, key=key, value=value)

  elif request.method == 'GET':
    return render_template("home.html", form=form, key=key, value=value, user=user)

@app.route("/results")
def results():
  if 'email' not in session:
    return redirect(url_for('login'))
  return render_template('results.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
