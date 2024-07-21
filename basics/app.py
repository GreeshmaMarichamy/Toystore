from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key="123"

def init_db():
    with sqlite3.connect("database.db") as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS customer (
                    pid INTEGER PRIMARY KEY,
                    firstname TEXT,
                    lastname TEXT,
                    email TEXT UNIQUE,
                    password TEXT
                    )
            """)

init_db()
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        firstname=request.form["firstname"]
        password=request.form["password"]

        with sqlite3.connect("database.db") as con:
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("SELECT * FROM customer WHERE firstname= ?",(firstname,))
            user=cur.fetchone()

        if user and check_password_hash(user['password'],password):
            session["user_id"]=user["pid"]
            session["firstname"]=user["firstname"]
            return redirect(url_for("home"))
        else:
            flash("Username and Password Mismatch")
            return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        try:
            firstname=request.form['firstname']
            lastname=request.form['lastname']
            email=request.form["email"]
            password=request.form["password"]
            confirmpassword=request.form["confirmpassword"]

            if password != confirmpassword:
                flash("Password do not match","danger")
                return redirect(url_for('register'))
            
            hashed_password=generate_password_hash(password)

            with sqlite3.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("""
                        INSERT INTO customer(
                            firstname,lastname,email,password)
                            VALUES(?,?,?,?)
                            """, (firstname,lastname,email,hashed_password))
                con.commit()
                flash("Added Successfully","success")
        except sqlite3.IntegrityError:
            flash("Email already exists","danger")
        except Exception as e:
            flash(f"Error in insert operation: {str(e)}","danger")
        finally:
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))  




@app.route("/toys")
def toys():
    return render_template("toys&games.html")

@app.route("/sports")
def sports():
    return render_template("sports&out.html")

@app.route("/zero")
def zero():
    return render_template("0-12.html")

@app.route("/barbie")
def barbie():
    return render_template("barbie.html")

@app.route("/lego")
def lego():
    return render_template("lego.html")


@app.route("/rideon")
def rideon():
    return render_template("rideon.html")

@app.route("/one")
def one():
    return render_template("1-3.html")

@app.route("/four")
def four():
    return render_template("4-7.html")

@app.route("/eight")
def eight():
    return render_template("8-10.html")

@app.route("/eleven")
def eleven():
    return render_template("11-14.html")

@app.route("/fourteen")
def fourteen():
    return render_template("14.html")

@app.route("/ham")
def ham():
    return render_template("hamleys.html")

@app.route("/customer")
def customer():
    if "user_id" in session:
        return render_template("customer.html",name=session["firstname"])
    else:
        return redirect(url_for("login"))

if __name__=='__main__':
    app.run(debug=True)