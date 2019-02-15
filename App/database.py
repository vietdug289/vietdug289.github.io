import sqlite3 
from sqlite3 import Cursor
#--------------

def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        print("Connect success !!!")
        return conn
    except Error as e:
        print(" Connect fail ")
    return None

def create_table(conn, execute_query):
    try: 
        cur = conn.cursor()
        cur.execute(execute_query)
        print("Create table success ")
    except Error as e:
        print(e)    



#---------------
if __name__ == "__main__":
    database = 'database.db'
    conn = create_connection(database)

    #---------------------
    create_table_user= """ 
    CREATE TABLE  IF NOT EXISTS user(
        id_user INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        gmail TEXT NOT NULL,
        address TEXT NOT NULL
    );
    """
    create_table(conn, create_table_user)
    print('1.user_table is done')
    #--------------------------
    create_table_subject= """ 
    CREATE TABLE  IF NOT EXISTS subject(
        id_subject INTEGER PRIMARY KEY,
        subject_name TEXT NOT NULL
    );
    """
    create_table(conn, create_table_subject)
    print('2.subject_table is done')
    #---------------
    create_table_class= """ 
    CREATE TABLE  IF NOT EXISTS class(
        id_class INTEGER PRIMARY KEY,
        class_name TEXT NOT NULL,
        subject_of_class TEXT NOT NULL,
        FOREIGN KEY (subject_of_class) REFERENCES subject(subject_name)
    );
    """
    create_table(conn, create_table_class)
    print('3.class_table is done')
    #-----------------
    create_table_choice= """ 
    CREATE TABLE  IF NOT EXISTS choice(
        id_choice INTEGER PRIMARY KEY,
        name_of_choice TEXT NOT NULL,
        class_name_of_choice TEXT NOT NULL,
        subject_name_of_choice TEXT NOT NULL,
        FOREIGN KEY (name_of_choice) REFERENCES user(name),
        FOREIGN KEY (class_name_of_choice) REFERENCES class(class_name)
    );
    """
    create_table(conn, create_table_choice)
    print('4.choice_table is done')
#__________________
    print("Complete database")