import MySQLdb
import MySQLdb.cursors
from flask import Flask, render_template, request, jsonify, json
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)

#mysql = MySQL(app)

@app.route("/",methods=['GET', 'POST'])
def main():
  if request.method == 'POST':
    db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    print("POST")
    try:
      print(request.data)
      parsed = json.loads(request.data)
      print(parsed)
      with open('G:/data.txt', 'w') as outfile:
        json.dump(parsed, outfile)
        outfile.close()
      title=parsed['title']
      print(title)
      year = parsed['year']
      print(year)
      authors = parsed['authors']
      print(authors)

      executeStr3 = 'Select id from book where title= %s and year = %s'
      row_count=cursor.execute(executeStr3,(title, year))
      print("row_count=" + str(row_count))
      cursorselectBook_fetchall=cursor.fetchall()
      print(cursorselectBook_fetchall)
      if len(cursorselectBook_fetchall)>0:
        print(str(cursorselectBook_fetchall[0])+" already exists")
     # print(cursorselectBook_fetchall[0]["id"])
      else:
        print("Add new book")
        query = "insert into book (title, year) values (%s,%s)"
        cursor.execute(query, (title, year))
        cursor.execute('''Select MAX(id) as maxid from book''')  # последний добавленный
        str_id_book = cursor.fetchone()
        #print(str_id_book)
        id_book=str_id_book['maxid']
        print(id_book)
        for author in authors:
         # for row in cursor.execute("select question_id, foo, bar from questions"):
         #   question_id, foo, bar = row
          print(author)
          cursor.execute('''Select id from author where name = %s''', [author])
          str_id_author=cursor.fetchone()
          print(str_id_author)
          id_author=0
          if str_id_author and str_id_author['id']:
            id_author=str_id_author['id']
            print(id_author)
          if not id_author:
            print("auhAdd")
            query = "insert into author (name) values (%s)"
            cursor.execute(query, [author])
            cursor.execute('''Select id from author where name = %s''', [author])
            id_author = cursor.fetchone()['id']
          print(id_author)
          query = "insert into book_author (id_book,id_author) values (%s,%s)"
          cursor.execute(query, (id_book,id_author))
    except:
    #  print("EXCEPTION!")
      return 'Error decoding json'
    db.commit()
    db.close()
    print("POST END")
    return 'Example'
  #return 'Hello!'
  if request.method == 'GET':
    print("GET")
    db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''Select * from book''')
    resultsBook = cursor.fetchall()
    result=json.dumps(resultsBook)
    db.commit()
    db.close()
    return result
  print("END")
  return 'Example'

@app.route("/books")
def books():
  if request.method == 'GET':
    print("GET BOOK")
    db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''Select * from book''')
    resultsBook = cursor.fetchall()
    result = json.dumps(resultsBook)
    db.commit()
    db.close()
    return result
@app.route("/authors")
def authors():
  if request.method == 'GET':
    print("GET AUTHOR")
    db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''Select * from author''')
    resultsAuthor = cursor.fetchall()
    result = json.dumps(resultsAuthor)
    db.commit()
    db.close()
    return result
@app.route("/output")
def out_data():
  db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
  cursor = db.cursor(MySQLdb.cursors.DictCursor)
  print("out_data")
  cursor.execute('''Select * from book''')
  resultsBook = cursor.fetchall()
  print(resultsBook)

  cursor.execute('''Select max(id) as mid from book''')
  resultsBook1 = cursor.fetchall()
  print(resultsBook1)
  if resultsBook1:
    print("resultsBook1_true")
    print(resultsBook1[0]["mid"])
  else:
    print("resultsBook1_false")

  cursor.execute('''Select * from author''')
  resultsAuthor = cursor.fetchall()

  cursor.execute('''SELECT book.title as title,
  book.year as year,
  GROUP_CONCAT(author.name) as name
FROM
  book_author ba
INNER JOIN
  book on book.id = ba.id_book
INNER JOIN
  author on author.id = ba.id_author
GROUP BY
  book.id''')
  resultsBookAuthor= cursor.fetchall()
  return render_template('output.html',resultsBook=resultsBook,resultsAuthor=resultsAuthor,resultsBookAuthor=resultsBookAuthor )
@app.route('/showSignUp')
def showSignUp():
  print("showSignUp")
  #call_find_all_sp()
  return render_template('signup.html')
@app.route('/actions',methods=['POST'])
def actions():
  if request.method == 'POST':
    print("POST actions")
    db = MySQLdb.connect(host="localhost", user="root", passwd="qwerty", db="bookauthor", charset='utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    print(request.data)
    parsed = json.loads(request.data)
    print(parsed)
    action = parsed['action']
    print(action)
    table = parsed['table']
    print(table)
    if action == 'delete':
      if table == 'book':
        cur_id = parsed['cur_id']
        cursor.execute("DELETE FROM book WHERE id= %s", [cur_id])
        cursor.execute("DELETE FROM book_author WHERE id_book= %s", [cur_id])
      elif table == 'author':
        cur_id = parsed['cur_id']
        print(cur_id)
        query1= "DELETE FROM author WHERE id=%s"
        #query1 = 'DELETE FROM %s WHERE id= %s'
        #query1 = "DELETE FROM %(table)s WHERE id=%(cur_id)s"

        print(query1)
        cursor.execute(query1, [cur_id])
        #cursor.execute(query1, (table,cur_id) )
        #cursor.execute(query1, {"table": str(table),"cur_id": cur_id})
        query2 = 'DELETE FROM book_author WHERE id_author= %s'
        print(query2)
        cursor.execute(query2, [cur_id])
      elif table == 'book_author':
        cur_id_book = parsed['cur_id_book']
        cur_id_author = parsed['cur_id_author']
        cursor.execute('''DELETE FROM book_author WHERE id_author=%s and id_book=%s''', (cur_id_author,cur_id_book))
    elif action=='update':
      if table=='book':
        cur_id = parsed['cur_id']
        title = parsed['title']
        year = parsed['year']
        cursor.execute('''Update book 
                          set title=%s,
                              year= %s 
                          where id=%s
                        ''',(title,year,cur_id))
      elif table=='author':
        cur_id = parsed['cur_id']
        name = parsed['name']
        cursor.execute('''Update author 
                          set name=%s 
                          where id=%s
                        ''', (name,cur_id))
      elif table == 'book_author':
        cur_id_book = parsed['cur_id_book']
        cur_id_author = parsed['cur_id_author']
        id_book = parsed['id_book']
        id_author = parsed['id_author']
        cursor.execute('''Update book_author 
                          set id_book=%s, 
                              id_author= %s 
                          where id_book=%s and id_author=%s 
                       ''', (id_book,id_author, cur_id_book,cur_id_author))
    db.commit()
    db.close()
  return 'Action page'

if __name__ == "__main__":
  app.run(debug=True)

