#Import Flask Library
from ntpath import join
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from hashlib import md5
import pymysql
from datetime import datetime, time, date
import time

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='airport',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

print("connection reached")

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/StaffloginAuth', methods=['GET', 'POST'])
def loginAuthAirlineStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'] #might have to hash this passoword###############
	

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['type'] = 'AirlineStaff' 
		return render_template('StaffHome.html')
		
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/StaffregisterAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	First_name = request.form['first_name']
	Last_name = request.form['last_name']
	Airline_name = request.form['airline_name']
	Date_of_birth = request.form['date_of_birth']
	phone_number = request.form['phone_number']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		first_name = request.form['first_name']
		last_name =request.form['last_name']
		username = request.form['username']
		password = request.form['password']
		date_of_birth = request.form['date_of_birth']
		airline_name = request.form['airline_name']
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return redirect('/') ###########################################################



def confirmstaff():
	if session.get('type') == 'AirlineStaff':
		query = "SELECT * FROM airline_staff WHERE username = %s"
		try:
			cursor = conn.cursor()
			cursor.execute(query, session['email'])
			data = cursor.fetchone()
			cursor.close()
			return len(data) > 0
		except:
			return False
			
	return False

#############################
#Create New Flights
@app.route('/StaffCreate')
def StaffCreate():
	if confirmstaff():
		cursor = conn.cursor()
		query = "INSERT INTO flight VALUES (%s %s %s %s %s %s %s %s)"
		cursor.execute(query, (request.form['flight_num'], request.form['airline_name'], 
		request.form['depart_date_time'], request.form['arrive_date_time'], request.form['base_price'],
		request.form['status'], request.form['depart_airport_code'], request.form['arrive_airport_code']))
		query = "SELECT * FROM airplane WHERE airline_name = %s"
		cursor.execute(query, request.form['airline_name'])
		planes = cursor.fetchall()
		return render_template("createflights.html", planes = planes)
	else:
		return redirect('/StaffHome') #After adding you can either logout or go home


@app.route('/StaffFlightView', methods = ['GET', 'POST'])
def StaffFlightLayout():
	if confirmstaff():
		"SELECT * from flight where depart_date_time >= {} AND depart_date_time <= {} AND airline_name = %s"
		cursor = conn.cursor()
		query = "SELECT airline_name, flight_num, depart_date_time, " \
		"arrive_date_time, depart_airport_code, arrive_airport_code, base_price, status FROM flight, " \
		"depart_airport_code AS leaving, arrive_airport_code AS arriving WHERE leaving.code = depart_airport_code " \
		"AND arriving = arrive_airport_code AND depart_date_time >= {}" \
		"AND depart_date_time <= {} AND airline_name = %s"
		cursor.execute(query (request.form['airline_name'], request.form['flight_num'], request.form['depart_date_time'],
		request.form['airrive_date_time'], request.form['depart_airport_code'], request.form['base_price'], request.form['status']))
		data = cursor.fetchall()

@app.route('/AddAirplane', methods = ["GET", "POST"])
def AddAirplane():
	print("accessing add airplane")
	if confirmstaff():
		cursor = conn.cursor()
		create = "INSERT into airplane VALUES(%s %s %s %s %s)"
		cursor.execute(create, request.form['id'], request.form['airline_name'], request.form['num_of_seats'], 
		request.form['manufacturing_comp'], request.form['airport_type'])
		conn.commit() # python does not auto commit, therefore need to send commit after making changes 
		cursor.close()
		return render_template('AddAirplane.html')
	else:
		return redirect('/logout') #After adding you can either logout or go home to perform more actions.


@app.route('/AddAirport', methods= ["GET", "POST"])
def AddAirport():
	if confirmstaff():
		cursor = conn.cursor()
		create = "INSERT into airport VALUES(%s %s %s %s %s)"
		cursor.execute(create, request.form['code'], request.form['airport_name'], request.form['city'],
		request.form['country'], request.form['airport_type'])
		conn.commit()
		data = cursor.fetchall()
		airports = "SELECT * FROM airport" 
		cursor.close()
		return render_template("AddAirport.html", data = data, airports = airports)
	else:
		return redirect('/logout') #After adding you can either logout or go home to perform more actions.

@app.route('/StaffHome')
def AirlineStaffHome():
	if confirmstaff():
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT username FROM airline_staff WHERE username = %s'
		cursor.execute(query, (username))
		return render_template("StaffHome.html", username=username)
	else:
		return redirect('/logout')

@app.route('/ViewFlights')
def StaffFlightView():
	if confirmstaff():
		return render_template("ViewFlights.html")
	return redirect('/logout')


		#############################

@app.route('/StaffChangeFlights', methods = ["GET", "POST"])
def StaffChangeFlights():
	if confirmstaff():
		cursor = conn.cursor()
		query =  "SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s"
		cursor.execute(query, (request.form['airline_name'], request.form['flight_num']))
		data = cursor.fetchall()
		if data:
			query = "UPDATE flight SET flight.status = %s WHERE airline_name = %s AND flight_num = %s"
			cursor.execute(query, (request.form['flight_status'], request.form['airline_name'], request.form['flight_num']))
			conn.commit()
			cursor.close()
			print("Successful Flight Status Change!")
			return redirect('/StaffHome')
		else:
			print("Error!")
	else:
		return redirect('/logout')


########################################


@app.route('/ViewFlightRatings', methods=["GET", "POST"])
def ViewFlightRatings():
	if confirmstaff():
		cursor = conn.cursor()
		average = "SELECT avg(ratings) as rating, comments, flight_num from rate natural"\
		"join flight natural join customer where airline_name = %s group by flight_num;"

		cursor.execute(average, request.form['airline_name'])
		data = cursor.fetchall()
		if data:
			return render_template('ViewFlightRatings.html', request.form['airline_name'], average=average)
		else:
			print("Error!")
	else:
		return redirect('/logout')

@app.route('/ViewEarnedRevenue', methods=["get"])
def ViewEarnedRevenue():
	if confirmstaff():
		cursor = conn.cursor()
		month = "SELECT sum(sold_price) as rev, purchase_date_time from ticket NATURAL JOIN purchase WHERE"\
		"purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 MONTH);"
		cursor.execute(month)
		past_month = cursor.fetchone()
		year = "SELECT sum(sold_price) as rev, purchase_date_time from ticket NATURAL JOIN purchase WHERE"\
		"purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 YEAR);"
		cursor.execute(year)
		past_year = cursor.fetchone()
		cursor.close()
		return render_template('ViewEarnedRevenue.html', past_month = past_month, past_year = past_year)
	else:
		return redirect('/logout')

@app.route('/ViewFrequentCustomers', methods=["get"])
def ViewFrequentCustomers():
	if confirmstaff():
		f

@app.route('/ViewTopDestinations', methods=["get"])
def ViewTopDestinations():
	if confirmstaff():
		cursor = conn.cursor()
		month = "SELECT arrival_airport_code, count(t.ticket_id) FROM purchase p JOIN ticket t ON f.flight_num = t.flight_num " \
                "JOIN purchase p ON t.ticket_id = p.ticket_id AND p.purchase_date_time >= DATE_SUB(NOW(), INTERVAL 3 MONTH " \
                "GROUP BY arrival_airport_name ORDER BY count(t.ticket_id) DESC LIMIT 3"
		cursor.execute(month, request.form['purchase_date'])
		past_three_months = cursor.fetchall()
		year = "SELECT arrival_airport_code, count(t.ticket_id) FROM flight f JOIN ticket t ON f.flight_num = t.flight_num " \
                "JOIN purchase p ON t.ticket_id = p.ticket_id AND p.purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 year " \
                "GROUP BY arrival_airport_name ORDER BY count(t.ticket_id) DESC LIMIT 3"
		cursor.execute(year, request.form['purchase_date'])
		past_year = cursor.fetchall()
		cursor.close()
		return render_template('ViewTopDestinations.html', past_three_months = past_three_months, past_year = past_year)
	else:
		return redirect('/logout')


'''
@app.route('/ViewReportsByTravelClass', method="get")
def ViewReportsByTravelClass():
	if confirmstaff():
		j

@app.route('/ViewReports', method="get")
def	ViewReports():
	if confirmstaff():
		cursor = conn.cursor()
		query = "SELECT count(t.ticket_id) FROM flight f JOIN ticket t ON f.flight_num = t.flight_num " \
                "JOIN purchase p ON t.ticket_id = p.ticket_id AND p.purchase_date >= %s"

'''
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
