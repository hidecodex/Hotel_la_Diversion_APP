from flask import Flask, render_template, request, redirect, url_for, flash, json
from flask_mysqldb import MySQL

app = Flask(__name__)

# mySQL conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hoteldiversion'
mysql = MySQL(app)

# Perfil
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas')
    data = cur.fetchall()
    
    return render_template('index.html', reserva = data)

@app.route('/templates/admin.html')
def Admin():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas')
    data = cur.fetchall()
    
    return render_template('admin.html', reserva = data)    

@app.route('/templates/reserva.html')
def reserva():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas')
    data = cur.fetchall()
    
    return render_template('reserva.html', reserva = data)     

@app.route('/templates/rooms.html')
def rooms():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas')
    data = cur.fetchall()
    
    return render_template('rooms.html', reserva = data) 

@app.route('/templates/loginAdmin.html')
def loginAdmin():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas')
    data = cur.fetchall()
    
    return render_template('loginAdmin.html', reserva = data)  

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
          

@app.route('/reservas', methods=['POST'])
def add_reserva():
    if request.method == 'POST':
        typeRoom = request.form['typeRoom']
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        days = request.form['days']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO reservas (typeRoom, fullname, phone, email, days) VALUES (%s, %s, %s, %s, %s)',
        (typeRoom, fullname, phone, email, days))

        mysql.connection.commit()

        flash('Reserva agregada correctamente')    
        return redirect(url_for('Index'))

@app.route('/editar/<id>')
def get_reservas(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit_reservas.html', reservas = data[0])

@app.route('/update/<id>', methods = ['POST'])  
def update_reserva(id):
    if request.method == 'POST':
      typeRoom = request.form['typeRoom']
      fullname = request.form['fullname']
      phone = request.form['phone']  
      email = request.form['email']
      days = request.form['days']    
    cur = mysql.connection.cursor()
    cur.execute("""
    UPDATE reservas
        SET typeRoom = %s,
        fullname = %s,
        phone = %s,
        email = %s,
        days = %s
        WHERE id = %s
    """, (typeRoom, fullname, phone, email, days, id))
    mysql.connection.commit()  
    flash('Reserva actualizada Correctamente')
    return redirect(url_for('Admin'))        

@app.route('/delete/<string:id>')
def delt_reservas(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM reservas WHERE id = {0}' .format(id))
   mysql.connection.commit()
   flash('Reserva eliminada correctamente')
   return redirect(url_for('Admin'))




if __name__ == '__main__':
    app.run(port=3000, debug=True)