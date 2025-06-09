import json
from flask import Flask, render_template, redirect, request, session, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import subprocess
import threading

# Firebase configuration
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# Flask app setup
app = Flask(__name__)
app.secret_key = "CustomerSupport@1234"  # Use an environment variable for production
app.config['upload_folder'] = os.path.join(os.getcwd(), 'static', 'upload')

# Route definitions
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/index')
def indexpage():
    return render_template("index.html")

@app.route('/logout')
def logoutpage():
    session.clear()
    return render_template("index.html")

@app.route('/about')
def aboutpage():
    return render_template("about.html")

@app.route('/services')
def servicespage():
    return render_template("services.html")

@app.route('/gallery')
def gallerypage():
    return render_template("gallery.html")

# Route for the login page
@app.route('/userlogin', methods=['GET'])
def userlogin():
    return render_template("userlogin.html", msg="")

# Route to handle login check
@app.route('/userlogincheck', methods=['POST'])
def userlogincheck():
    try:
        uname = request.form['uname']
        pwd = request.form['pwd']
        db = firestore.client()
        newdb_ref = db.collection('newuser')
        dbdata = newdb_ref.get()
        for doc in dbdata:
            data = doc.to_dict()
            if data['UserName'] == uname and data['Password'] == pwd:
                session['userid'] = data['id']
                return render_template("usermainpage.html")
        return render_template("userlogin.html", msg="Invalid Username/Password")
    except Exception as e:
        return render_template("userlogin.html", msg=f"Error: {e}")

@app.route('/newuser')
def newuser():
    return render_template("newuser.html", msg="")

# Route for adding new users
@app.route('/addnewuser', methods=['POST'])
def addnewuser():
    try:
        fname = request.form['fname']
        lname = request.form['lname']
        uname = request.form['uname']
        pwd = request.form['pwd']
        email = request.form['email']
        phnum = request.form['phnum']
        address = request.form['address']
        id = str(random.randint(1000, 9999))
        json_data = {
            'id': id, 'FirstName': fname, 'LastName': lname,
            'UserName': uname, 'Password': pwd, 'EmailId': email,
            'PhoneNumber': phnum, 'Address': address
        }
        db = firestore.client()
        newuser_ref = db.collection('newuser')
        newuser_ref.document(id).set(json_data)
        return render_template("newuser.html", msg="New User Added Successfully")
    except Exception as e:
        return render_template("newuser.html", msg=f"Error: {e}")

@app.route('/contact', methods=['POST', 'GET'])
def contactpage():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            id = str(random.randint(1000, 9999))
            json_data = {
                'id': id, 'ContactName': name, 'Message': message,
                'Subject': subject, 'EmailId': email
            }
            db = firestore.client()
            db.collection('newcontact').document(id).set(json_data)
            return render_template("contact.html", msg="Contact Added Successfully")
        return render_template("contact.html")
    except Exception as e:
        return render_template("contact.html", msg=f"Error: {e}")

@app.route('/userviewprofile')
def userviewprofile():
    try:
        user_id = session.get('userid')
        if not user_id:
            return redirect(url_for('userlogin'))
        db = firestore.client()
        user_data = db.collection('newuser').document(user_id).get().to_dict()
        return render_template("userviewprofile.html", data=user_data)
    except Exception as e:
        return render_template("userviewprofile.html", msg=f"Error: {e}")

@app.route('/detector')
def detector():
    return redirect("http://localhost:8502", code=302)

# Function to run Streamlit
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.headless", "true"])

# Main function
if __name__ == '__main__':
    threading.Thread(target=run_streamlit, daemon=True).start()
    app.debug = True
    app.run()
