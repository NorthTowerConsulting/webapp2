from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import mysql
import mysql.connector as sql_db

app = Flask(__name__, template_folder="template")
#Configure Database
app.config["MYSQL_HOST"] = "invoice-database-server.mysql.database.azure.com"
app.config["MYSQL_USER"] = "elliott"
app.config["MYSQL_PASSWORD"] = "Apprentice123!"
app.config["MYSQL_DB"] = "invoice_schema"
app.config["MYSQL_SSL"] = "DigiCertGlobalRootCA.crt.pem"
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/add-an-invoice",methods=["GET", "POST"])
def add():
    if request.method == "POST":
        invoicenumber = request.form["invoicenumber"]
        name = request.form["name"]
        address = request.form["address"]
        description = request.form["description"]
        invoicetotal = request.form["invoicetotal"]  
        date = request.form["date"]      

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO invoices (name, address, date, invoicenumber, description, invoicetotal) VALUES (%s, %s, %s, %s, %s, %s)", [name, address, date, invoicenumber, description, invoicetotal])
        mysql.connection.commit()
    return render_template("invoice-add.html")

@app.route("/view-invoices")
def view():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM invoices")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template("invoices.html", userDetails=userDetails)
    else:
        return render_template("no-invoices.html")
    
@app.route('/delete/<string:id_number>', methods = ['POST', 'GET'])
def delete(id_number):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM invoices WHERE id = %s", (id_number))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/edit-invoices', methods = ['POST', 'GET'])
def edit():
    if request.method == 'POST':
        invoicenumber = request.form['invoicenumber']
        id_number = request.form['id']
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        invoicetotal = request.form['invoicetotal']
        date = request.form['date']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE invoices SET invoicenumber=%s,name=%s, address=%s, description=%s, invoicetotal=%s, date=%sWHERE id=%s", (id_number, invoicenumber, name, address,description,invoicetotal, date))
        mysql.connection.commit()
        
    return render_template ("invoice-edit.html")
if __name__ == "__main__":
    app.run(debug=True)
