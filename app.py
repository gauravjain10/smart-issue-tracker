from flask import Flask, render_template, request, url_for, session, redirect
from flask_mysqldb import MySQL
import MySQLdb
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import DateField, StringField, TextAreaField, SubmitField ,validators
from flask_wtf.file import FileField, FileRequired
from wtforms_components import TimeField
from werkzeug.utils import secure_filename
from main import function,ehealthforumQAs_function
from preprocessing import preprocess
import os
import subprocess
import massedit
import re
import fileinput
import pandas as pd

SECRET_KEY = os.urandom(32)
app = Flask(__name__, template_folder='templates')   
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "login"

db = MySQL(app)


#class MyForm(FlaskForm):
    #question = TextAreaField("query", validators=[DataRequired()])
    #submit = SubmitField('submit')



@app.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('home.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        if "username" in request.form and "password" in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor =  db.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute("INSERT INTO login.credentials(email,password) VALUES(%s,%s)",(username,password))
                db.connection.commit()
                return redirect(url_for('login'))
            except:
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tncs', methods=('GET', 'POST'))
def tncs():
    return render_template('tncs.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username'] 
            password = request.form['password'] 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM credentials WHERE email=%s AND password=%s",(username,password))
            credentials = cursor.fetchone()
            if credentials is not None:     
                if credentials['email'] == username and credentials['password'] == password:
                    session['loginfailure'] = False
                    return redirect(url_for('user'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/user', methods=('GET', 'POST'))
def user():
    if session['loginfailure'] == False:
        return render_template('user.html')

@app.route('/covid', methods=('GET', 'POST'))
def covid():
    return render_template('covid.html')

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop("loginfailure", None)
    return render_template('logout.html')

@app.route('/ehealthforumQAs', methods=('GET', 'POST'))
def ehealthforumQAs():
    return render_template('ehealthforumQAs.html')

@app.route('/answer',methods = ['GET', 'POST'])
def answer():
    global question
    question = request.form['query']
    #save(question)
    q = preprocess(question)
    if len(q)==0:
        return "Please enter a vaild question"
    else:
        A,Q,score = function(q)
    
    r1= A[0]
    r2= A[1]
    r3= A[2]
    
    q1=Q[0]
    q2=Q[1]
    q3=Q[2]
    
    sc1=score[0]
    sc2=score[1]
    sc3=score[2]
    #return question
    #return render_template('answer.html',)
    return render_template("result.html",Question=question,Q1=q1,A1=r1,S1=sc1,Q2=q2,A2=r2,S2=sc2,Q3=q3,A3=r3,S3=sc3)
    
@app.route('/ehealthforumQAs_answer',methods = ['GET', 'POST'])
def ehealthforumQAs_answer():
    global question
    question = request.form['query']
    #save(question)
    q = preprocess(question)
    if len(q)==0:
        return "Please enter a vaild question"
    else:
        A,Q,score = ehealthforumQAs_function(q)
    
    r1= A[0]
    r2= A[1]
    r3= A[2]
    
    q1=Q[0]
    q2=Q[1]
    q3=Q[2]
    
    sc1=score[0]
    sc2=score[1]
    sc3=score[2]
    #return question
    #return render_template('answer.html',)
    return render_template("result.html",Question=question,Q1=q1,A1=r1,S1=sc1,Q2=q2,A2=r2,S2=sc2,Q3=q3,A3=r3,S3=sc3)

def save(text, filepath='question.txt'):
    with open("question.txt", "a") as f:
        f.write('\n')
        f.write(text)


@app.route('/save_que', methods=['GET', 'POST'])
def save_que(filepath='save_question.txt'):
    df = pd.read_csv("unanswered_q.csv")
    df.loc[-1]= question
    df.to_csv("unanswered_q.csv",index=False)
    return render_template('home.html')

@app.route('/unanswered', methods=('GET', 'POST'))
def unanswered():
    df = pd.read_csv("unanswered_q.csv")
    qlist=list(df['0'])
    return render_template('unanswered.html',l=qlist,n = len(qlist))

@app.route('/save_qa', methods=('GET', 'POST'))
def save_qa():
    ans = request.form['exans']
    que = request.form['que']
    remove_question(que)
    df=pd.read_csv('new_qa.csv')
    df.loc[-1]=que,ans
    df.to_csv("new_qa.csv",index=False)
    return render_template('save_qa.html',q=que,a=ans)


def remove_question(question):
    df = pd.read_csv("unanswered_q.csv")
    df=df[df['0']!=question]
    df.to_csv("unanswered_q.csv",index=False)

if __name__ == '__main__':
    app.run(debug = True)
