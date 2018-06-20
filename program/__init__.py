import MySQLdb
import MySQLdb.cursors
from flask import Flask, render_template, request, jsonify, json
from flask_mysqldb import MySQL
import requests

#from python_mysql_dbconfig import read_db_config

def call_find_all_sp():
  try:
    db_config = read_db_config()
    conn = MySQLConnection(**db_config)
    cursor = conn.cursor()

    cursor.callproc('find_all')

    # print out the result
    for result in cursor.stored_results():
      print(result.fetchall())

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

app = Flask(__name__)

db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
#mysql = MySQL(app)

@app.route("/",methods=['GET', 'POST'])
def main():
  if request.method == 'POST':
    parsed = json.loads(request.data)

    with open('C:/data.txt', 'w') as outfile:
      json.dump(parsed, outfile)
      outfile.close()
  #ОТПРАВИТЬ ВСЕ ЗНАЧЕНИЯ ТАБЛИЦ
  cursor = db.cursor()
  #cursor.execute('''SELECT user, host FROM mysql.user''')
  cursor.execute('''SELECT * FROM book''')
  rv = cursor.fetchall()
  return str(rv)
  #return 'Hello!'
  if request.method == 'GET':
    jsonstr = {"newkey": "newvalue"}
  return jsonstr
@app.route("/index")
def index():
  return render_template("index.html")


@app.route('/showSignUp')
def showSignUp():
  #call_find_all_sp()
  return render_template('signup.html')

if __name__ == "__main__":
  app.run(debug=True)

