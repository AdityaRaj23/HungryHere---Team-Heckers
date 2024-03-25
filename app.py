from flask import Flask, render_template, request, redirect, session
import re
from urllib.parse import urlsplit
import requests
import json
from flask_session import Session
import json
from pymongo.mongo_client import MongoClient
import urllib.parse
username = urllib.parse.quote_plus('TeamSOS')
password = urllib.parse.quote_plus('noKPkgEGaVYFqGYC')

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY']="HereIsTheBest"
Session(app)

def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    if not session.get("name"):
        return redirect("/login")
    return render_template('map.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        client=MongoClient("mongodb+srv://%s:%s@fid.f8e3plo.mongodb.net/?retryWrites=true&w=majority" % (username, password))
        user=client["hungryhere"]
        userlogin=user["login"]
        a=list(userlogin.find({"email":request.form.get("email"), "password":request.form.get("password")}))
        if len(a)>0:
            print("sed")
            session["name"] =a[0]['name']
            return redirect('/map')
        else:
            return render_template("login.html", error="sed")
    return render_template("login.html")
 
@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        print(request.form.get("password"))
        client=MongoClient("mongodb+srv://%s:%s@fid.f8e3plo.mongodb.net/?retryWrites=true&w=majority" % (username, password))
        user=client["hungryhere"]
        userlogin=user["login"]
        if len(list(userlogin.find({"name":request.form.get("name")})))>0:
            print("magik")
            return render_template("register.html", error="sed")
        else:
            val={"name":request.form.get("name"),"password":request.form.get("password"),"email":request.form.get("email")}
            userlogin.insert_one(val)
            return redirect('/login')
    return render_template("signup.html")


if __name__ == "__main__":
    context=('/etc/ssl/certs/fullchain.crt', '/etc/ssl/private/www.sociotrackr.live.key')
    app.run(debug=True, port=5000, host="0.0.0.0",ssl_context=context)
