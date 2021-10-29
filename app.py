import re
import random
from flask import Flask,render_template,request
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



@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/user_registration",methods=['GET','POST'])
def user_registration():
    if request.method=="POST":
        uid=random.randint(1000,9999)
        upass=request.form['pass']
        ufname=request.form['fname']
        ulname=request.form['lname']
        umobile=request.form['phone']
        uaadhar=request.form['aadharno']
        users = users_db(uid=uid,ufname=ufname,ulname=ulname,umobile=umobile,uaadhar=uaadhar,upass=upass)
        db.session.add(users)
        db.session.commit()
    return render_template("user_registration.html")

@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

@app.route("/hospital_login")
def hospital_login():
    return render_template("hospital_login.html")

@app.route("/show")
def show():
    allUsers=users_db.query.all()
    print(allUsers)
    return "<p>This is show page</p>"

@app.route("/products")
def products():
    return "<p>This is products page</p>"

if __name__=="__main__":
    app.run(debug=True)