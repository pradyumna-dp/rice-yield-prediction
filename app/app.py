from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from accuracy import predict_accuracy
from prediction import predict_production
from features import soil_data,weather
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)

# Mailer
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'robynx.podcast@gmail.com'
app.config['MAIL_PASSWORD'] = 'koonitrosrnzitmx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# SQL Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bapp'
mysql = MySQL(app)


@app.route('/')
def select():
    return render_template('select.html')

@app.route('/dashboard/<disctrict>')
def dashboard(disctrict):
    prediction= predict_accuracy(disctrict)
    predicted_value = round(prediction,3)
    production_prev = predict_production(disctrict,2021)
    production_next = predict_production(disctrict,2022)
    soil_info = soil_data(disctrict)
    disct = disctrict.title()
    temparature = weather(disct)
    if temparature > 0:
        temparature = weather(disct)
    else:
        temparature = 25
    return render_template('dashboard.html',dist_name=disct,accuracy=predicted_value,previous=production_prev,next=production_next,soil_values=soil_info,temp=temparature)

@app.route('/subscribe',methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        disctrict = request.form['district']
        current_date = date.today()
        msg = Message('Hello '+name, sender = 'yourId@gmail.com', recipients = [email])
        msg.body = "Hello "+name+" thanks for Subscribing to bapp constant updates on "+disctrict+" will be sent to this mail"
        mail.send(msg)
        response = {'message': 'Thank you for subscribing'}
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users(name, email, district, date) VALUES(%s, %s, %s, %s)', (name, email, disctrict, current_date))
        mysql.connection.commit()
        cursor.close()
        return jsonify(response)
    
if __name__ == '__main__':
   app.run(debug = True)