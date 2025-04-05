from flask import Flask,request,jsonify, Blueprint
from database import db


import requests
login_app=Blueprint('login_app',__name__)


class User(db.Model):#Defines a database table called user
    id= db.Column(db.Integer,primary_key=True)#makes unique auto incrementing id's
    first_name=db.Column(db.String(100),unique=False,nullable=False)#storing first name
    second_name=db.Column(db.String(100),unique=False,nullable=False)#storing last name
    email=db.Column(db.String(100),unique=True,nullable=False)#making unique email
    password=db.Column(db.String(500),nullable=False)#making passwords(saving as plain text for now)
    def __repr__(self,jhr3 ):#(used for debugging)
        return f"<User {self.email}>"


#making login route

@login_app.route("/login",methods=["POST"])
def cust_login(): 
    data=request.get_json()
    cust_username=data.get("email")
    cust_pass=data.get("password")
    user=User.query.filter_by(email=cust_username).first()
    if user and user.password == cust_pass:
        return jsonify({"message":"login is successful!","username":user.email}),200
    else:
        return jsonify({"message":"Invalid credentials "}),401
#making register route

@login_app.route("/register",methods=["POST"])
def cust_register():
    data=request.get_json()
    cust_first= data.get("first_name")
    cust_second = data.get("second_name")
    cust_username=data.get("email")
    cust_pass= data.get("password")
   
    
    user=User(first_name=cust_first,second_name=cust_second,email=cust_username,password=cust_pass)
    db.session.add(user)
    db.session.commit()
    return jsonify("User registered successfully")

#making users table route

@login_app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Get all users from the database
    # Convert the users to a list of dictionaries
    users_list = [{"id": user.id, "first name": user.first_name,"last name": user.second_name, "username": user.email, "password": user.password} for user in users]
    return jsonify(users_list)  # Return the list of users as JSON




