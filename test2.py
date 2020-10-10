import sqlite3
try:
    conn=sqlite3.connect('testingdb.db')
    cur=conn.cursor()
    for i in cur.execute('''select * from testing;'''):
        print(i)
    conn.close()
except:
    print('error opening the database')