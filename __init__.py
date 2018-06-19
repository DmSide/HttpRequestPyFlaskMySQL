#import MySQLdb
#import MySQLdb.cursors
from flask import Flask, render_template, request, jsonify, json
#import json
import requests

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def main():
  if request.method == 'POST':
    parsed = json.loads(request.data)

    with open('C:/data.txt', 'w') as outfile:
      json.dump(parsed, outfile)
      outfile.close()
  return 'Hello!'
@app.route("/index")
def index():
  return render_template("index.html")
if __name__ == "__main__":
  app.run(debug=True)