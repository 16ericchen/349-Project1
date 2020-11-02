from flask import Flask
from flask import render_template
from flask import request,redirect
import sys
from werkzeug.utils import secure_filename
import sqlite3 as sql
import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = os.getcwd() + '\\static\\img\\'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'dbase.db')

with sql.connect(my_file) as db:
      cursor = db.cursor()
      sqql = ''' CREATE TABLE IF NOT EXISTS NEW( name text, email text, food_name, img);'''
      cursor.execute(sqql)
      db.commit()

def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def convertToBinaryData(filename):
      with open(filename, 'rb') as file:
            blobData = file.read()
            return blobData

@app.route('/',methods = ['POST', 'GET'])
def submission():
   if request.method == 'POST':
         name = request.form['username']   
         email = request.form['usermail']
         food_name = request.form['foodtyp']
         img = request.files['upload']
         filename = secure_filename(img.filename)
         img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         imgDIR = os.getcwd() + '\\static\\img\\'+filename
         filelocation = 'img/'+filename
         convertToBinaryData(imgDIR)
         con = sql.connect('dbase.db')
         cur = con.cursor() 
         cur.execute("INSERT INTO NEW(name,email,food_name,img) Values (?,?,?,?)",(' '+name+' ', email+' ', food_name+' ',filelocation))
         con.commit()
         cur.execute("SELECT * FROM NEW ORDER BY rowid DESC LIMIT 1")
         row1 = cur.fetchone()
         print(row1)
         cur.execute("SELECT * FROM NEW ORDER BY RANDOM() LIMIT 100;")
         row2 =cur.fetchone()
         con.close()     
         return render_template('index.html',row1 = row1,row2 = row2)
   else:
      return render_template('submission-page.html')


@app.route('/index/')
def index():
            connection = sql.connect('dbase.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM NEW ORDER BY RANDOM() LIMIT 1000;")
            row1 = cursor.fetchone()
            print(row1)
            row2 = cursor.fetchone()
            cursor.close() 
            return render_template('index.html',row1 = row1,row2 = row2)














