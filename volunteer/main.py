import psycopg2
from flask import Flask, render_template, g, request, redirect, url_for
from flask import Blueprint
from . import db

bp=Blueprint("volunteer", "volunteer", url_prefix="/volunteer")

@bp.route("/reg", methods=["GET", "POST"])
def register():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="GET":
        return render_template("register.html")
    elif request.method=="POST":
        userid =request.form.get("u_id")
        uname=request.form.get("name")
        udob=request.form.get("dob")
        uemail=request.form.get("email")
        umobileno=request.form.get("mobileno")
        uusertype=request.form.get("usertype")
        uyearofstudy=request.form.get("yearofstudy")
        udept=request.form.get("dept")
        upassword=request.form.get("password")
        upsw_repeat=request.form.get("psw_repeat")
        if (upassword == upsw_repeat):
            cursor.execute("insert into users (u_id,name,dob,email,mobileno,usertype,yearofstudy,dept,password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid,uname,udob,uemail,umobileno,uusertype,uyearofstudy,udept,upassword))
            if (uusertype == 'Student'):
                cursor.execute("insert into student(stu_id,yearofstudy) values (%s,%s)",(userid,uyearofstudy))
            if (uusertype == 'Admin'):
                cursor.execute("insert into administrator(adm_id,dept) values (%s,%s)",(userid,udept))         
    dbconn.commit()
    return redirect(url_for("volunteer.login"),302)
@bp.route("/login",methods=["GET", "POST"])
def login():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="POST":
        userid=request.form.get("u_id")
        p_word=request.form.get("password")
        cursor.execute("select * from users where u_id=(%s) and password=(%s)",(userid,p_word,))
        retrieved=cursor.fetchall()
        strlen=len(retrieved)
        if (strlen==1):
            cursor.execute("select usertype from users where u_id=(%s) and password=(%s)",(userid,p_word,))
            utype=cursor.fetchone()[0]
            if(utype=='Student'):
                 return render_template("studenthome.html",userid=userid)
            else:
                 return render_template("AdminHome.html",userid=userid)
        else:
            return render_template("login.html")
    elif request.method=="GET":
            return render_template("login.html")
    dbconn.commit()
@bp.route("/add", methods=["GET", "POST"])
def add_activity():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="GET":
        return render_template("addactivity.html")
    elif request.method=="POST":
        userid=request.form.get("userid")
        title=request.form.get("title")
        skills=request.form.get("skills")
        description=request.form.get("description")
        startdate=request.form.get("startdate")
        enddate=request.form.get("enddate")
        cursor.execute("insert into activities (adm_id,title,skills,description,startdate,enddate) values (%s,%s,%s,%s,%s,%s)",(userid,title,skills,description,startdate,enddate,))
        dbconn.commit()
        return render_template("index.html")
@bp.route("/view")
def view_activities():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select * from activities order by enddate asc")
    tasks=cursor.fetchall()
    return render_template("tasklist.html", tasks=tasks)


    
    
if __name__=="__main__":
    app.run()
