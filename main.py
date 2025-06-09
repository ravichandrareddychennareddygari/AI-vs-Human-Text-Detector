
import json
from difflib import get_close_matches
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
from flask import Flask, render_template, redirect, request, session, url_for
from flask import Flask, render_template
import firebase_admin
import random
from firebase_admin import credentials
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1 import FieldFilter
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)

app.secret_key="CustomerSuport@1234"
app.config['upload_folder']='/static/upload'

@app.route('/')
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/index')
def indexpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logoutpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/about')
def aboutpage():
    try:
        return render_template("about.html")
    except Exception as e:
        return str(e)

@app.route('/usermainpage')
def usermainpage():
    try:
        return render_template("usermainpage.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logout():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)


@app.route('/services')
def servicespage():
    try:
        return render_template("services.html")
    except Exception as e:
        return str(e)

@app.route('/gallery')
def gallerypage():
    try:
        return render_template("gallery.html")
    except Exception as e:
        return str(e)


@app.route('/userlogincheck', methods=['POST'])
def userlogincheck():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            print("Uname : ", uname, " Pwd : ", pwd);
            newdb_ref = db.collection('newuser')
            dbdata = newdb_ref.get()
            data = []
            flag = False
            for doc in dbdata:
                #print(doc.to_dict())
                #print(f'{doc.id} => {doc.to_dict()}')
                #data.append(doc.to_dict())
                data = doc.to_dict()
                if(data['UserName']==uname and data['Password']==pwd):
                    flag=True
                    session['userid']=data['id']
                    break
            if(flag):
                print("Login Success")
                return render_template("usermainpage.html")
            else:
                return render_template("userlogin.html", msg="UserName/Password is Invalid")
    except Exception as e:
        return render_template("userlogin.html", msg=e)


@app.route('/userlogin',methods=["POST","GET"])
def userloginpage():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            newdb_ref = db.collection('newuser')
            dbdata = newdb_ref.get()
            flag = False
            for doc in dbdata:
                data = doc.to_dict()
                if (data['UserName'] == uname and data['Password'] == pwd):
                    flag = True
                    session['userid'] = data['id']
                    break
            if (flag):
                print("Login Success")
                return render_template("usermainpage.html")
            else:
                return render_template("userlogin.html", msg="UserName/Password is Invalid")
        return render_template("userlogin.html")
    except Exception as e:
        return str(e)


@app.route('/newuser')
def newuser():
    try:
        msg=""
        return render_template("newuser.html", msg=msg)
    except Exception as e:
        return str(e)

@app.route('/addnewuser', methods=['POST',"GET"])
def addnewuser():
    try:
        print("Add New User page")
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phnum']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName':lname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newuser')
            id = json['id']
            newuser_ref.document(id).set(json)
        return render_template("newuser.html", msg="New User Added Success")
    except Exception as e:
        return str(e)


@app.route('/contact',methods=['POST','GET'])
def contactpage():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'ContactName': name,
                    'Message': message, 'Subject': subject,
                    'EmailId': email}
            db = firestore.client()
            db_ref = db.collection('newcontact')
            id = json['id']
            db_ref.document(id).set(json)
            msg="Contact Added Success"
            return render_template("contact.html",msg=msg)
        else:
            return render_template("contact.html")
    except Exception as e:
        return str(e)

@app.route('/userviewprofile')
def userviewprofile():
    try:
        id=session['userid']
        print("Id",id)
        db = firestore.client()
        newdb_ref = db.collection('newuser')
        data = newdb_ref.document(id).get().to_dict()
        print(data)
        return render_template("userviewprofile.html", data=data)
    except Exception as e:
        return str(e)
        return render_template("userviewprofile.html", msg=e)
    


    # New route to handle the Detector click
@app.route('/detector')
def detector():
    # Redirect to the Streamlit app
    return redirect("http://localhost:25502", code=302)

if __name__ == '__main__':
    app.debug = True
    app.run()
