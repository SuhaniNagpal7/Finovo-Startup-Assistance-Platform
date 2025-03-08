from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
import sqlite3
import random
import os
from website.investormail import *
from website.otp import *
from website.startupmail import *
from website.investormail import *
from website.meetinvestor import *
from website.meetstartup import *
# from website.Valuation_prediction_for_funding import *

auth = Blueprint('auth', __name__)



con1 = sqlite3.connect("basics.db",check_same_thread=False)
con2 = sqlite3.connect("startup.db",check_same_thread=False)
con3 = sqlite3.connect("investor.db",check_same_thread=False)

basic = con1.cursor()
startup = con2.cursor()
investor = con3.cursor()

login = False
user = []
otpsent = 0
em=0
typ = 0

basic.execute("CREATE TABLE IF NOT EXISTS login( namee varchar,email varchar,password varchar, atype varchar  )")
basic.execute("CREATE TABLE IF NOT EXISTS requests(namee varchar,email varchar,atype varchar)")

startup.execute("CREATE TABLE IF NOT EXISTS startups( namee varchar,description varchar)")

@auth.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@auth.route('/form1', methods=['GET', 'POST'])
def form1():

    return render_template("Form1.html", user=current_user)

# @auth.route('/form2', methods=['GET', 'POST'])
# def form2():
#     username = request.form.get('username')
#     date = request.form.get('date')
#     industry = request.form.get('industry')
#     location = request.form.get('location')
#     type = request.form.get('type')
#     ed = (username,date,industry,location,type)
#     prediction1(ed)
#     return render_template("form2.html", user=current_user)
#


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global login
    if login != True:
       if request.method == "POST":
            email = request.form.get('emailornum')
            password = request.form.get('password')
            basic.execute("select * from login")
            my_data = basic.fetchall()
            msc = 0
            record = []
            global typ
            global user
            for i in my_data:
                print(i)
                if email in i:
                    msc += 1
                    record = i
                    break
                else:
                    continue
            user = record
            if msc == 0:
                flash('Invalid Email or Username', category='error')

            else:
                if password != record[2]:
                    flash('Incorrect password', category='error')
                else:
                    if record[3] == "investor":

                          typ = "investor"
                          return redirect(url_for('auth.investorhome'))
                    elif record[3] == "startup":
                          typ = "startup"
                          return redirect(url_for('auth.startuphome'))

    else:
        return redirect(url_for('auth.homesort'))

    return render_template("login.html", user=current_user)


@auth.route('/startuphome', methods=['GET', 'POST'])
def startuphome():
    return render_template("startuphome.html", user=current_user)

@auth.route('/startupdetails', methods=['GET', 'POST'])
def startupdetails():
    return render_template("startupdetails.html", user=current_user)


@auth.route('/investorhome', methods=['GET', 'POST'])
def investorhome():
    return render_template("investorhome.html", user=current_user)

@auth.route('/sysoon', methods=['GET', 'POST'])
def sysoon():
    return render_template("sysoon.html", user=current_user)

@auth.route('/models', methods=['GET', 'POST'])
def models():
    f=["45.897655","1000000"]
    return render_template("models.html", user=current_user,data=f)



@auth.route('/startuplist', methods=['GET', 'POST'])
def startuplist():
    startup.execute("select distinct * from startups")
    f=startup.fetchall()
    return render_template("startuplist.html", user=current_user,data=f)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    global login
    if login!= True:
     if request.method == "POST":
        basic.execute("select * from login")

        my_data = basic.fetchall()
        email = request.form.get('email')
        name = request.form.get('name')
        atype = request.form.get('type')
        print(email,name,atype)
        msc = 0
        for i in my_data:
            print(i)
            if email in i:
                msc += 1
                break
            else:
                continue

        basic.execute("select * from requests")
        my_data = basic.fetchall()
        ms = 0
        for i in my_data:
            print(i)
            if email in i:
                ms += 1
                break
            else:
                continue

        if msc != 0 or ms !=0 :
            flash('Email Already in use', category='error')
        else :
           if atype.lower()=="investor" or atype.lower()=="startup" :
               global user
               global em
               em = email
               user.append(email)
               user.append(name)
               user.append(atype)
               global otpsent
               otpsent = random.randint(100000,999999)
               send_otp(otpsent,email)
               return redirect(url_for('auth.otp'))


    return render_template("signup.html", user=current_user)


@auth.route('/homesort', methods=['GET', 'POST'])
def homesort():
    global typ
    if typ == "investor":
            return redirect(url_for('auth.investorhome'))
    elif typ == "startup":
            return redirect(url_for('auth.startuphome'))

    return 0


@auth.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method =="POST" :
        global otpsent
        eotp = request.form.get('eotp')
        global user
        if not eotp.isdigit() or len(eotp)!=6:
            flash("Invalid otp", category="error")
        else:
            if int(eotp)!=otpsent:
                flash("Incorrect Otp",category="error")
            else :
                basic.execute("insert into requests values ('{}','{}','{}')".format(user[1],user[0],user[2]))
                con1.commit()
                global em
                if user[2] == "investor":
                        investormail(em)
                else :
                   startupmail(em)
                return redirect(url_for('auth.sysoon'))

    return render_template("otp.html", user=current_user)




@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    global user
    user = []
    return redirect(url_for('auth.home'))

@auth.route('/vrmeet', methods=['GET', 'POST'])
def vrmeet():
    global em
    meetinvestor(em)
    meetstartup()
    return redirect(url_for('auth.homesort'))

@auth.route('/vrmeeting', methods=['GET', 'POST'])
def vrmeeting():
    return render_template("vrmeet.html", user=current_user)







