import sqlite3
from sqlite3 import Error
from random import randint
 
def create_connection(db_file):
 
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all_questions(conn):
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM quiz")
 
    rows = cur.fetchall()
    size = len(rows)
    num = randint(3,10)
    #print(num)
    cur.execute("SELECT * FROM quiz WHERE id = {}".format(num))
    question = cur.fetchall()
    return question
    
def main_def():
    database = "quiz_data.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        return select_all_questions(conn)
 
 
#if __name__ == '__main__':
 #   main()
