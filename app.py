import re
import random
from flask import Flask,render_template,request
from flask.sessions import NullSession
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///users_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class users_db(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    ufname=db.Column(db.String(200),nullable=True)
    ulname=db.Column(db.String(200),nullable=True)
    umobile=db.Column(db.String(10),nullable=True)
    uaadhar=db.Column(db.String(12),nullable=True)
    upass=db.Column(db.String(200),nullable=True)
    def __repr__(self) -> str:
        return f"{self.uid} - {self.ufname}"

class appointments(db.Model):
    uid=db.Column(db.Integer,db.ForeignKey('users_db.uid'),primary_key=True)
    name=db.Column(db.String(200),nullable=True)
    state=db.Column(db.String(200),nullable=True)
    city=db.Column(db.String(200),nullable=True)
    hospital=db.Column(db.String(100),nullable=True)
    date=db.Column(db.String(100),nullable=True)
    def __repr__(self) -> str:
        return f"{self.uid} - {self.ufname}"

class blood(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    ufname=db.Column(db.String(200),nullable=True)
    ublood=db.Column(db.String(12),nullable=True)
    ustate=db.Column(db.String(200),nullable=True)
    ucity=db.Column(db.String(200),nullable=True)
    def __repr__(self) -> str:
        return f"{self.uid} - {self.ufname}"

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/user_registration",methods=['GET','POST'])
def user_registration():
    ruid=0
    if request.method=="POST":
        uid=random.randint(1000,9999)
        ruid=uid
        upass=request.form['pass']
        ufname=request.form['fname']
        ulname=request.form['lname']
        umobile=request.form['phone']
        uaadhar=request.form['aadharno']
        users = users_db(uid=uid,ufname=ufname,ulname=ulname,umobile=umobile,uaadhar=uaadhar,upass=upass)
        db.session.add(users)
        db.session.commit()
    return render_template("user_registration.html",ruid=ruid)

@app.route("/book_appointments",methods=['GET','POST'])
def appointment_details():
    if request.method=="POST":
        uid=request.form['uid']
        name=request.form['name']
        state=request.form['state']
        city=request.form['city']
        hospital=request.form['hospital']
        date=str(request.form['meeting'])
        print(city)
        appointment=appointments(uid=uid,name=name,state=state,city=city,hospital=hospital,date=date)
        db.session.add(appointment)
        db.session.commit()
    return render_template("appointment_details.html")

@app.route("/user_login",methods=['GET','POST'])
def user_login():
    if request.method=="POST":
        uid=request.form['uid']
        upass=request.form['pass']
        user= users_db.query.filter_by(uid=uid).first()
        if(user is None):
            return '''<head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"></head><a href='/user_login'><button class="btn btn-warning" style="padding:30px;margin:20px">Try again</button></a><script>function f(){alert('Entered username/password is incorrect please try again')}; f();</script>'''
        if(user.upass==upass):
            return render_template("user_homepage.html")
            
    return render_template("user_login.html")

@app.route("/hospital_login")
def hospital_login():
    return render_template("hospital_login.html")


@app.route("/request_for_blood",methods=['GET','POST'])
def request_for_blood():
    if request.method=="POST":
        uid=request.form['phid']
        ufname=request.form['pname']
        ublood=request.form['pblood']
        ustate=request.form['state']
        ucity=request.form['city']
        bloods=blood(ufname=ufname,uid=uid,ublood=ublood,ustate=ustate,ucity=ucity)
        db.session.add(bloods)
        db.session.commit()   
        return render_template("blood_request.html")   
    return render_template("blood_request.html")

@app.route("/user_homepage")
def user_homepage():
    return render_template("user_homepage.html")

@app.route("/blood_search")
def blood_search():
    users= blood.query.all()
    return render_template("blood_search.html",bg=users)

@app.route("/upload_health")
def upload_health():
    return render_template("upload_health.html")

@app.route("/hospital_homepage")
def hospital_homepage():
    return render_template("hospital_homepage.html")

# @app.route("/request_for_blood")
# def request_for_blood():
#     return "<h1>This is under development</h1>"

@app.route("/patient_search",methods=['GET','POST'])
def patient_search():
    usr={}
    if request.method=="POST":
        name=request.form['name']
        users= users_db.query.filter_by(ufname=name)
        # users= users_db.query(users_db.uid,users_db.ufname,users_db.ulname,users_db.umobile,users_db.uaadhar,appointments.state,appointments.city,appointments.hospital,appointments.date).join(users_db).join(appointments).filter_by(users_db.ufname==name)
        return render_template("patient_search.html",users=users)
    return render_template("patient_search.html")

@app.route("/patient_appointments_search",methods=['GET','POST'])
def patient_appointments_search():
    usr={}
    if request.method=="POST":
        name=request.form['name']
        appointment= appointments.query.filter_by(name=name)
        # users= users_db.query(users_db.uid,users_db.ufname,users_db.ulname,users_db.umobile,users_db.uaadhar,appointments.state,appointments.city,appointments.hospital,appointments.date).join(users_db).join(appointments).filter_by(users_db.ufname==name)
        return render_template("patient_appointments_search.html",appo=appointment)
    return render_template("patient_appointments_search.html")

@app.route("/show")
def show():
    allUsers=users_db.query.all()
    print(allUsers)
    return "<p>This is show page</p>"


if __name__=="__main__":
    app.run(debug=True)