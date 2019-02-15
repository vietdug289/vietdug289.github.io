from flask import Flask, request,render_template, url_for,flash
from flask import session,redirect
import sqlite3 as sql

#--------------------------------------------------------------
app = Flask(__name__)
database= "database.db"
app.debug = True
app.secret_key="Nguyen Viet Dung"
#--------------------------------------------------------------

@app.route('/home/list-of-user/')
def index():
    if "username" in session:
        username = session['username']
        with sql.connect(database) as conn:
            cur = conn.cursor()
            getall_query  ="SELECT * FROM '%(tablename)s' "
            table={
                "tablename":"user"
            }
            cur.execute(getall_query %table)
            data = cur.fetchall()
            for row in data:
                print(row)

            return render_template("index.html", data = data, username=username)
    print("You are not logged in !!")
    return "<h1>WElcome</h1>"
def get_username(id):
    with sql.connect(database) as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM user WHERE id_user ='%(id)s'")
        name = cur.fetchone()
        return name

@app.route('/home/infor/<id>', methods=["POST","GET"])
def get_infor(id):
    print(id) 
    result =None
    result2=None
    username = session["username"]
    if "username" in session:
        with sql.connect(database) as conn:
            cur = conn.cursor()
            getall_query  ="SELECT * FROM user WHERE id_user='%(id)s' "
            getclass_query = ""
            data={
                "id":id
            }
            cur.execute(getall_query %data)
            result = cur.fetchone()
            print(result)
        with sql.connect(database)  as conn:
            cur = conn.cursor()   
            data2={
                "name": get_username(id)
            }
            get_class_querry = "SELECT * FROM choice WHERE name_of_choice ='%(name)s'"
            cur.execute(get_class_querry %data2)
            result2 = cur.fetchall()
        return render_template("infor.html",result= result, result2 = result2)
    return "<h1>WElcome</h1>"

@app.route('/home/infor/<id>/change', methods=["POST","GET"])
def change_infor(id):
    id = id
    if request.method =="POST":
        with sql.connect(database) as conn:
            cursor =conn.cursor()
            data={      
                    "name":request.form["name"],
                    "password":request.form["password"],
                    "gmail":request.form["gmail"],
                    "address": request.form["address"],
                    "id":id
                }
            change_query = "UPDATE user SET password= '%(password)s', name= '%(name)s', gmail = '%(gmail)s', address='%(address)s' WHERE id_user='%(id)s'"
            cursor.execute(change_query %data)
            conn.commit()
            print("sucsess")
            return redirect(url_for('get_infor',id=id))
    return redirect(url_for('get_infor',id= id))
    

@app.route('/home/information/') 
def getusername():
    if "username" in session:
        username = session['username']
        result =None
        result2 =None
        with sql.connect(database) as conn:
            cur = conn.cursor()
            getall_query  ="SELECT * FROM user WHERE username='%(username)s' "
            data={
                "username":username
            }
            cur.execute(getall_query %data)
            result = cur.fetchone()
            print(result)
        with sql.connect(database ) as conn:
            cur =  conn.cursor()
            data2={
                "username" :username
            }
            get_class_querry = "SELECT * FROM choice WHERE name_of_choice ='%(username)s'"
            cur.execute(get_class_querry %data2)
            result2 = cur.fetchall()
        return render_template("infor.html",result= result, result2 = result2)
    return redirect(url_for('index'))
@app.route('/home/information/delete/<classname>')
def delete_class(classname):
    username = session["username"]
    with sql.connect(database) as conn:       
        cur = conn.cursor()
        data={
                "username":username,
                "classname":classname
        }
        print(data)
        delete_query ="delete from choice where name_of_choice='%(username)s' and class_name_of_choice = '%(classname)s'"
        cur.execute(delete_query %data)
        conn.commit()
        print("suceess")
        return redirect(url_for('getusername'))
    return redirect(url_for('getusername'))
#--------------------------------------------------
@app.route('/',methods=["POST","GET"])
@app.route('/login',methods=["POST", "GET"])
def login():
    if "username" in session:
        print("User in session")
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
        
            data = {
                "username" : request.form['username'],
                "password": request.form['password']
            }
            check_query = "SELECT * FROM user WHERE user.username='%(username)s' and user.password='%(password)s'"
            with sql.connect(database) as conn:
                cur = conn.cursor()
                cur.execute(check_query %data)
                results = cur.fetchone()
                if results == None:
                    print("No data")
                    return render_template('login.html')
                else:
                    session['username'] = request.form['username']
                    print('Get data from html sucessfully.')
                    print(results)
                    return  redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('login'))
#--------------------------------------------------------------------
#TODO: writing function register new menber __________________________done =V
def check_user(data):
    check_query = "SELECT * FROM user WHERE user.username='%(username)s' "
    with sql.connect(database) as conn:
        cur = conn.cursor()
        cur.execute(check_query %data)
        results= cur.fetchone()
        if results  == None:
            print("Register successfully!")
            return True
        return False
    return False   

@app.route('/register',methods=["POST","GET"])
def register():
    if request.method=="POST":
        check_data={
            "username":request.form['username']
        }
        if check_user(check_data) == True:
            data={
                "username":request.form["username"],
                "password" :request.form["password"],
                "name": request.form["name"],
                "gmail":request.form["gmail"],
                "address":request.form["address"]
            }
            input_sql ="INSERT INTO user(username, password, name, gmail, address) VALUES('%(username)s', '%(password)s','%(name)s','%(gmail)s','%(address)s')"
            with sql.connect(database) as conn:
                cursor = conn.cursor()
                cursor.execute(input_sql %data)
                conn.commit() 
                print("create new user sucessfully")
                session["username"] = request.form["username"]
                return redirect(url_for('index'))
        else:
            print("Fail")
    return render_template('register.html')

@app.route('/home/')
@app.route("/home/List-of-subject/")
def getallsubject():
    if "username" in session:
        with sql.connect(database) as conn:
            getall_query = " SELECT subject_name FROM subject"
            cur = conn.cursor()
            cur.execute(getall_query)
            results = cur.fetchall()
        return render_template("listofsubject.html", results=results)

@app.route("/home/List-of-subject/<subjectname>")
def getclassbysubject(subjectname):
    result= None
    with sql.connect(database) as conn:
        cur = conn.cursor()
        data={
            "subject": subjectname
        }
        get_query = "Select * from class where subject_of_class ='%(subject)s'"
        cur.execute(get_query % data)
        result = cur.fetchall()
    return render_template("classwithsubject.html", result = result, subjectname= subjectname)

@app.route('/home/list-of-class/')
def get_all_class():
    if "username" in session:
        with sql.connect(database) as conn:
            cur = conn.cursor()
            data={
                "name_of_choice": session["username"]
            }
            select_query="select distinct *  from class where class.class_name not in (select choice.class_name_of_choice from choice where choice.name_of_choice='%(name_of_choice)s')"
            
            cur.execute(select_query %data)
            data_of_class = cur.fetchall()
            print(data_of_class)
            if data_of_class == []:
                mess = "No data"    
                username= session["username"]
                return render_template("listofclass.html", mess= mess, username = username)
            else:
                mess =""
                return render_template("listofclass.html", data_of_class = data_of_class , mess=mess)
    return "<h1> welcome<h1>"

#ham dang ki mon hoc
@app.route('/home/list-of-class/submit', methods=["POST","GET"])
def submit_class():
    if request.method =="POST":
        username = session["username"]
        choices = request.form.getlist('choices')
        class_name = None
        subject_of_class = None
        for i in choices:
            #get class from class_id 
            with sql.connect(database) as conn:
                cur = conn.cursor()
                data ={
                    "id_class": i
                }
                get_query ="SELECT class_name, subject_of_class FROM class WHERE class.id_class = '%(id_class)s'"
                cur.execute(get_query %data)
                value = cur.fetchone()
                class_name = value[0]
                subject_of_class = value[1]
            data={
                    "name_of_choice": username,
                    "class_name_of_choice":class_name,
                    "subject_name_of_choice": subject_of_class,
            }
            print(data)
            with sql.connect(database) as conn:
                cur = conn.cursor()
                submit_query ="INSERT INTO choice(name_of_choice, class_name_of_choice,subject_name_of_choice) VALUES('%(name_of_choice)s','%(class_name_of_choice)s','%(subject_name_of_choice)s')"
                cur.execute(submit_query %data)
                conn.commit()
                print("sucess")
                mess = "sucesss"
        return redirect(url_for('get_all_class'))
        
    return redirect(url_for('get_all_class'))

@app.route('/home/list-of-class/create-new-class/')
def create_new_class():
    if "username" in session:
        with sql.connect(database) as conn:
            cur= conn.cursor()
            cur.execute("SELECT subject_name from subject")
            subject_name = cur.fetchall()
            return render_template("createclass.html", subject_name =subject_name)
    return "<h1> welcome<h1>"

@app.route('/save', methods=["POST","GET"])   
def save():
    
    if request.method =="POST":
        data = {
            "class_name" :  request.form['name'],
            "subject_of_class": request.form.getlist('subjects')[0]
        }
        print(data)
        with sql.connect(database) as conn:
            cur = conn.cursor()
            save_query ="INSERT INTO class(class_name, subject_of_class) VALUES('%(class_name)s','%(subject_of_class)s')"
            cur.execute(save_query %data)
            conn.commit()
            print("sucess")
        return redirect(url_for('get_all_class'))
    return redirect(url_for('create_new_class'))

if __name__ == "__main__":
    app.run(port=8094)






