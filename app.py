from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3

import bert


app = Flask(__name__)
app.secret_key = "mykey123"

@app.route('/', methods=['GET', 'POST'])
def Home():
    return render_template('Login.html')

@app.route('/Login',methods = ['GET','POST'])
def Login():
    r = ""
    msg = ""

    if (request.method == "POST"):
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("grammar.db")
        c = conn.cursor()
        c.execute("SELECT * FROM userinfo WHERE email = '" + email + "' and password ='" + password + "'")
        r = c.fetchall()

        for i in r:
            if (email == i[1] and password == i[2]):
                session["log"] = True
                session["email"] = email.split('@')[0]
                return redirect(url_for("checker"))
            else:
                msg = "please enter valid username and password"

    return render_template('Login.html')



@app.route('/Signup', methods=['GET','POST'])
def Signup():
    msg = None
    if (request.method == "POST"):
        if (request.form["username"] != "" and request.form["email"] != "" and request.form["password"] != ""):
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            conn = sqlite3.connect("grammar.db")
            c = conn.cursor()
            c.execute("INSERT INTO userinfo VALUES('" + username + "','" + email + "','" + password + "')")
            msg = "Your account is created"


        else:
            msg = "Something wents wrong"
        conn.commit()
        conn.close()
        return redirect(url_for('Login'))

    return render_template("Signup.html", msg=msg)





@app.route('/checker', methods=['GET','POST'])
def checker():

    if(request.method == 'POST'):
        '''
            For rendering results on HTML GUI
            '''
        inp_string = [x for x in request.form.values()]
        sent = inp_string[0]
        index = bert.bert_checker(sent)
        # index2 = ULMFIT.UFMFIT_checker(sent)[1]
        print("here1")
        output = "perfect" if index == 1 else "not right!!"
        # output2 = "perfect" if index2 == 1 else "not right!!"
        print("here2")

        return render_template('checker.html', prediction_bert=' "{}" is grammatically {}'.format(sent, output))

    return render_template('checker.html')



@app.route("/Contact", methods=["GET", "POST"])
def Contact():
    msg = None
    if (request.method == "POST"):
        if (request.form["name"] != "" and request.form["email"] != "" and request.form["message"] != ""):
            name = request.form["name"]
            email = request.form["email"]
            message = request.form["message"]

            conn = sqlite3.connect("grammar.db")
            c = conn.cursor()
            c.execute("INSERT INTO cont VALUES('" + name + "','" + email + "','" + message + "')")
            msg = "Your response has been recorded"
            conn.commit()
            conn.close
        else:
            msg = "Something wents wrong"
    return render_template("Contact.html", msg=msg)

@app.route("/About",methods =["GET","POST"])
def About():
      if request.method == ['POST']:
            return redirect(url_for("contact"))
            return redirect(url_for("About"))
            return redirect(url_for("Login"))
      return render_template("About.html")





if __name__ == "__main__":
    app.run(debug=True)
