#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 01:27:52 2020

@author: dilsher
"""

from flask import Flask
from flask import render_template
from flask import request, jsonify


import os

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "student_info.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    student_id = db.Column(db.String(10),  nullable=False, primary_key=True)
    first_name = db.Column(db.String(80),  nullable=False, primary_key=False)
    last_name = db.Column(db.String(80),  nullable=False, primary_key=False)
    dob = db.Column(db.String(10),  nullable=False, primary_key=False)
    amount_due = db.Column(db.Float,  nullable=False, primary_key=False)
    
    def __init__(self, student_id, first_name, last_name, dob, amount_due):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due
        
    def __repr__(self):
        return f"Student('{self.student_id}', '{self.first_name}','{self.last_name}', '{self.dob}', '{self.amount_due}')"

class StudentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('student_id', 'first_name', 'last_name', 'dob', 'amount_due')


user_schema = StudentSchema()
users_schema = StudentSchema(many=True)
    
def get_latest_id():    
    students = Student.query.all()
    student_last_id =int(students[-1].student_id)
    return student_last_id + 1


@app.route("/",methods=["GET"])
def get_student_list():
    students = Student.query.all()
    result = users_schema.dump(students)
    return jsonify(result)
    #return render_template("student_form.html", students = students)

# endpoint to get user detail by id
@app.route("/<id>", methods=["GET"])
def student_detail(id):
    id = str(id)
    student = Student.query.get(id)
    return user_schema.jsonify(student)



@app.route("/",methods=["POST"])
def home():
    if request.form:
        id = get_latest_id()
        student = Student(student_id = id,
                          first_name=request.form.get("fname"),
                          last_name = request.form.get("lname"),
                          dob = request.form.get("dob"),
                          amount_due = request.form.get("amt"))
        
        db.session.add(student)
        db.session.commit()
        
        print(request.form)
    return user_schema.jsonify(student)
  
    
# endpoint to update user
@app.route("/<id>", methods=["PUT"])
def user_update(id):
    id = str(id)
    student = Student.query.get(id)
    amount = request.json['amt']
    
    student.amount_due = amount
    
    db.session.commit()
    return user_schema.jsonify(student)

# endpoint to delete user
@app.route("/<id>", methods=["DELETE"])
def user_delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return user_schema.jsonify(student)

if __name__ == "__main__":
    app.run(debug=True)
