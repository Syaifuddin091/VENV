from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskdb"
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route("/mahasiswa", methods=['GET', 'POST'])
def dashboard():
    title = "Form Mandling"
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print("Email yang dikirim adalah", email)
        print("Username yang dikirim adalah", username)
        print("Password yang dikirim adalah", password)
        return render_template('index.html', title=title)
    return render_template('dashboard.html', title=title)

@app.route("/mhs", methods=['GET'])
def mhs():
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM mahasiswa") 
    data = curr.fetchall()
    curr.close()
    print("data mahasiswa", data)
    return render_template('mhs.html', mahasiswa=data)

@app.route("/add_mahasiswa", methods=['POST'])
def add_mahasiswa():
    id_mahasiswa = request.form['id_mahasiswa']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    alamat = request.form['alamat']

    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM mahasiswa WHERE id_mahasiswa=%s", (id_mahasiswa,))
    existing_mahasiswa = curr.fetchone()
    
    if existing_mahasiswa:
        curr.close()
        return "ID Mahasiswa sudah ada. Silakan gunakan ID yang berbeda.", 400

    curr.execute("INSERT INTO mahasiswa (id_mahasiswa, username, password, email, alamat) VALUES (%s, %s, %s, %s, %s)", 
                 (id_mahasiswa, username, password, email, alamat))
    mysql.connection.commit()
    curr.close()
    return redirect(url_for('mhs'))

@app.route("/update_mahasiswa/<int:id>", methods=['GET', 'POST'])
def update_mahasiswa(id):
    curr = mysql.connection.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        alamat = request.form['alamat']

        curr.execute("UPDATE mahasiswa SET username=%s, password=%s, email=%s, alamat=%s WHERE id_mahasiswa=%s", 
                     (username, password, email, alamat, id))
        mysql.connection.commit()
        curr.close()
        flash("Data mahasiswa berhasil diperbarui.", "success")
        return redirect(url_for('mhs'))

    curr.execute("SELECT * FROM mahasiswa WHERE id_mahasiswa=%s", (id,))
    mahasiswa = curr.fetchone()
    curr.close()
    
    return render_template('update.html', mahasiswa=mahasiswa)

@app.route("/delete_mahasiswa/<int:id>", methods=['POST'])
def delete_mahasiswa(id):
    curr = mysql.connection.cursor()
    curr.execute("DELETE FROM mahasiswa WHERE id_mahasiswa=%s", (id,))
    mysql.connection.commit()
    curr.close()
    flash("Data mahasiswa berhasil dihapus.", "success")
    return redirect(url_for('mhs'))

if __name__ == '__main__':
    app.run(debug=True)