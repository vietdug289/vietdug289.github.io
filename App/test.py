import sqlite3 as sql 

database= 'database.db'
def test():
    with sql.connect(database) as conn:
        cur = conn.cursor()
        select_query = "SELECT user.id_user FROM user WHERE user.username='admin' "
        cur.execute(select_query)
        data = cur.fetchone()
        print(type(data[0]))

def getselfinfor():
    
    with sql.connect(database) as conn:
        cur = conn.cursor()
        getall_query  ="SELECT * FROM user WHERE username='%(username)s' "
        data={
            "username":"admin"
        }
        cur.execute(getall_query %data)
        result = cur.fetchone()
        for i in result:
            if i != result[0]:
                print(i)

def get_all_class():
   
    with sql.connect(database) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        data_of_class = cur.fetchall()
        mess = "No data"
        print(data_of_class != [])

def create_new_class():
    subjectname =()
    with sql.connect(database) as conn:
        cur= conn.cursor()
        cur.execute("SELECT subject_name from subject")
        subjectname = cur.fetchall()
    print(subjectname[0][0])

def get_subject(classname):
    data={
        "classname" : classname
    }
    with sql.connect(database) as conn:
        cur = conn.cursor()
        get_query= "SELECT subject_of_class FROM CLASS WHERE class_name = '%(classname)s'"
        cur.execute(get_query %data)
        subject_name = cur.fetchone()
    print(subject_name[0])
    print(type(subject_name[0]))


def get_tuple():
    str1= "(1, 'Legal 1', 'Legal')"
    a=[]
    for i in str1:
        if i !='(' :
            print(i)
            a.append(i)
get_tuple()