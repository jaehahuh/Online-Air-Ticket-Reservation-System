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



########################################################## public view, Register and customer ##############################################################
#Authenticates the register
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def custoRegisterAuth():
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor()
    
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, (email))
        data = cursor.fetchone()
        error = None

        if(data):
            #if customer is already exist in data
            error = "Already a registered user."
            return render_template('register.html', error = error)

        #if new customer
        name = request.form['name']
        addr_building_num = request.form['addr_building_num']
        addr_street = request.form['addr_street']
        addr_city = request.form['addr_city']
        addr_state = request.form['addr_state']
        phone_num = request.form['phone_num']
        passport_num = request.form['passport_num']
        passport_exp = request.form['passport_exp']
        passport_country = request.form['passport_country']
        date_of_birth = request.form['date_of_birth']
        inst = 'INSERT into customer values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(inst, (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth))
        conn.commit()
        cursor.close()
    
        return render_template('index.html')


@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def stafRegisterAuth():
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()

        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
        error = None

        
        if(data):

            #if staff is already exist in data
            error = "Already a registered staff."
            return render_template('register.html', error = error)




        airline_name = request.form['airline_name']
        query = 'SELECT * FROM airline WHERE airline_name = %s'
        cursor.execute(query, (airline_name))
        
        if not cursor.fetchone():
            error = "This airline does not exists"
            return render_template('register.html', error = error)


        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_nums = request.form['phone_nums'].split(', ')
        
        inst = 'INSERT into airline_staff values (%s, %s, %s, %s, %s, %s)'
        cursor.execute(inst, (username, airline_name, password, first_name, last_name, date_of_birth))

        for number in phone_nums:
            ins = 'INSERT into staff_phone_num values (%s, %s)'
            cursor.execute(inst, (username, number))

        conn.commit()
        cursor.close()
    
        return render_template('index.html')



#View public info
@app.route('/public_view_info', methods=['GET', 'POST'])
def searchPublicView():
        cursor = conn.cursor()

    
        query = 'SELECT distinct f.airline_name, f.flight_num, de.airport_name as depart_airport, \
        f.depart_date_time, ar.airport_name as arrive_airport, f.arrive_date_time, f.status, f.airplane_id \
        FROM flight f, airport de, airport ar \
        WHERE f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code \
        AND f.depart_airport_code = %s AND f.arrive_airport_code = %s \
        ORDER BY f.depart_date_time'
        cursor.execute(query, (request.form['depart_airport_code'], request.form['arrive_airport_code']))
        '''
        if "return_date" in request.form:
                return_date = request.form['return_date']
                query =  'SELECT distinct f.airline_name, f.flight_num, de.airport_name as depart_airport, \
                f.depart_date_time, ar.airport_name as arrive_airport, f.arrive_date_time, f.status \
                FROM flight f, airport de, airport ar \
               WHERE f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code \
                AND depart_airport = %s AND arrive_airport = %s AND return_date = %s AND return_date>= CURRENT_TIMESTAMP\
                ORDER BY f.depart_date_time)'
        '''

        conn.commit()
        data1 = cursor.fetchall()
        for each in data1:
                print(each)

        cursor.close()
        return render_template('index.html', public_flight_info=data1)


#Define route for customer home
@app.route('/custo_home')
def custo_home():
        username = session['username']
        cursor = conn.cursor();
        query = 'SELECT name FROM customer WHERE email = %s'
        cursor.execute(query, (username))
        custo_name = cursor.fetchone()
        return render_template('custo_home.html', name=custo_name['name'])


@app.route('/custo_search_flight', methods=['GET', 'POST'])
def search_flights_customer():
    cursor = conn.cursor();

    
    query =  'SELECT distinct f.airline_name, f.flight_num, de.airport_name as depart_airport, \
    f.depart_date_time, ar.airport_name as arrive_airport, f.arrive_date_time, f.base_price\
    FROM flight f, airport de, airport ar \
    WHERE f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code \
    AND depart_airport = %s AND arrive_airport = %s\
    ORDER BY f.depart_date_time)'
    cursor.execute(query, (request.form['depart_airport_code'], request.form['arrive_airport_code']))
    conn.commit()
    data1 = cursor.fetchall()
    for each in data1:
        if each['depart_date_time'] <= datetime.now():
            each['access'] = 1
        print(each)
    query = 'select name from customer where email = %s'
    cursor.execute(query, (username))
    custo_name = cursor.fetchone() 
    cursor.close()
    return render_template('custo_home.html', custo_flight_info=data1, name=custo_name['name'])


#Define a route to buyhome
@app.route('/buyhome/<flight_num>/<airline_name>', methods=['GET', 'POST'])
def buyhome(flight_num, airline_name):
        print(flight_num, airline_name)
        return render_template('buying_ticket.html', flight_num=flight_num, airline_name=airline_name)

#Define a route for buy ticket
@app.route('/buying_ticket/<flight_num>/<airline_name>', methods=['GET', 'POST'])
def buyTicket(flight_num, airline_name):
        cursor = conn.cursor()
        username = session['username']
        card_num = request.form['card_num']
        card_type = request.form['card_type']
        card_name = request.form['card_name']
        card_exp = request.form['card_exp']
        query = 'SELECT max(ticket_id) From ticket'
        cursor.execute(query)
        ticket_id = cursor.fetchone()['max(ticket_id)'] + 1
        query = 'SELECT * from Flight WHERE flight_num = %s'
        cursor.execute(query, (flight_num))
        flight_info = cursor.fetchone()
        query = 'SELECT num_of_seats FROM airplane Where flight_num = %s'
        cursor.execute(query, (flight_num))
        seats = cursor.fetchone()['num_of_seats']
        depart_date = flight_info['depart_date_time']

        if depart_date <= datetime.now() or ticket_id >= seats:
                query = 'SELECT name FROM customer WHERE email = %s'
                cursor.execute(query, (username))
                custo_name = cursor.fetchone()
                return render_template('custo_home.html', name=custo_name['name'])

        base_price = flight_info['base_price']
        if ticket_id/seats >= 0.75:
                query = 'UPDATE flight SET base_price = %s where flight_num = %s'
                base_price *= 1.25
                cursor.execute(query, (base_price, flight_num))
        query = 'INSERT into ticket values (%s, %s, %s, %s, %s)'
        cursor.execute(query, (ticket_id, airline_name, flight_num, depart_date, base_price))
        query = 'INSERT into purchase values (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (username, ticket_id, card_num, card_type, card_name, card_exp, datetime.now()))
        return render_template('buyticket.html')
       

#Define route for rating
@app.route('/rating')
def rate():
        username = session['username']
        cursor = conn.cursor()
        query = 'SELECT distinct airline_name, flight_num, depart_date_time, ratings, comments FROM rate WHERE email = %s'
        cursor.execute(query, (username))
        rates = cursor.fetchall()
        for line in rates:
                print(line)
        return render_template('rating.html', rates=rates)



#Write new rates and comments 
@app.route('/newRating', methods=['GET', "POST"])
def newRate():
        username = session['username']
        airline_name = request.form['airline_name']
        flight_num = request.form['flight_num']
        dept_date = request.form['depart_date_time']
        rate = request.form['rating']
        comment = request.form['comment']
        cursor = conn.cursor()
        query = 'SELECT * FROM ticket NATURAL JOIN purchase WHERE flight_num = %s and email = %s'
        cursor.execute(query, (flight_num, username))
        exist1 = cursor.fetchall()
        error = None

        if not exist1:
                error = "You cannot rate this flight since you did not take the flight."
                return render_template('rating.html', error=error)
        query = 'SELECT * FROM flight WHERE flight_num = %s and depart_date_time < SYSDATE()'
        cursor.execute(query, (flight_num))
        exist2 = cursor.fetchall()
        error = None
        if not exist2:
                error = "You cannot rate this flight since the flight has not departed yet."
                return render_template('rating.html', error=error)
        query  = 'INSERT into rate values(%s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (flight_num, username, rate, comment))
        print(cursor.fetchall())
        conn.commit()
        cursor.close()
        return redirect(url_for('rating'))



# Define a route for history
@app.route('/custo_history')
def history():
        cursor = conn.cursor()
        username = request.form['username']
        query = 'SELECT sum(sold_price) FROM purchase WHERE email = %s and purchase_date_time between date_sub(now(), interval 1 year)'
        cursor.execute(query, (username))
        year_spent = cursor.fetchone()
        year_spent = year_spent.get('sum(sold_price)')

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        curr_month = datetime.now().month - 1
        past_six_month = {}
        rest = 0
        if curr_month - 6 < 0:
                rest = (curr_month - 6) * -1
                for i in range(6 - rest):
                        past_six_month[months[curr_month - i]] = 0
                for i in range(rest):
                        past_six_month[months[i]] = 0
        else:
                for i in range(6):
                        past_six_month[months[curr_month - i]] = 0
        for month in past_six_month:
                query = 'SELECT sum(sold_price) FROM purchase where email = %s and monthname(purchase_date_time) = %s'
                cursor.execute(query, (username, month))
                total_spent_month = cursor.fetchone()
                total_spent_month = total_spent_month.get('sum(sold_price)')
        if total_spent_month:
                past_six_month[month] = total_spent_month

    #History of Past flights
        query = 'SELECT DISTINCT f.airline_name, f.flight_num, de.airport_name as depart_airport, f.depart_date_time, ar.airport_name as arrive_airport, f.arrive_date_time \
                FROM flight f, airport de, airport ar, (purchase p NATURAL JOIN ticket t) \
                WHERE (f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND p.ticket_id = t.ticket_id AND t.flight_num = f.flight_num AND p.email = %s \
                ORDER BY f.depart_date_time'
        cursor.execute(query, (username))
        flights_history = cursor.fetchall()
        return render_template('custo_history.html', year_spent=year_spent, past_six_month=past_six_month, flights_history = flights_history)


#view total amount of money spent within that range
@app.route('/history_by_range', methods=['GET', 'POST'])
def historyByRange():
        username = session['username']
        cursor = conn.cursor()
    
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_month = start_date.split('-')[2] + ' ' + datetime.strptime(start_date.split('-')[1], '%m').strftime('%B')
        end_month = end_date.split('-')[2] + ' ' + datetime.strptime(end_date.split('-')[1], '%m').strftime('%B')

        if start_date > end_date:
                return redirect(url_for('history'))

        query = 'SELECT sum(sold.price) FROM ticket NATURAL JOIN purchase WHERE email = %s and purchase_date_time between date(%s) and date (%s)'
        cursor.execute(query, (username, start_date, end_date))
        total_spent = cursor.fetchone()['sum(sold_price)']
    
        query = 'SELECT date(purchase_date_time), ticket_id, sold_price as sale_price From ticket NATURAL JOIN purchase \
                WHERE email = %s and date(purchase_date_time) between date(%s) and date(%s)'
        cursor.execute(query, (username, start_date, end_date))
        history_date = cursor.fetchall()
        for line in history_date:
                print(line)
        return render_template('custo_history.html', total_spent_interval=total_spent, start_month=start_month, end_month=end_month, history_date=history_date)



###################################################################Login and staff #########################################################
@app.route('/StaffloginAuth', methods=['GET', 'POST'])
def loginAuthAirlineStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'] #might have to hash this passoword###############
	

	#cursor used to send queries
	with conn.cursor() as cursor:
	#cursor = conn.cursor()
	#executes query
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
		cursor.execute(query, (username, password))
		#stores the results in a variable
		data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

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

@app.route('/CustomerloginAuth', methods=['GET', 'POST'])
def loginAuthCustomer():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'] #might have to hash this passoword###############
	

	#cursor used to send queries
	with conn.cursor() as cursor:
	#cursor = conn.cursor()
	#executes query
		query = 'SELECT * FROM customer WHERE email = %s and password = %s'
		cursor.execute(query, (username, password))
		#stores the results in a variable
		data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['type'] = 'Customer' 
		return render_template('custo_home.html')
		
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)



def confirmstaff():
	print(session.get('type'))
	if session.get('type') == 'AirlineStaff':
		query = "SELECT * FROM airline_staff WHERE username = %s"
		print('Our query is: ', query)
		try:
			cursor = conn.cursor()
			print('Our session is: ', session)
			cursor.execute(query, session.get('username'))
			data = cursor.fetchone()
			cursor.close()
			return len(data) > 0
		except:
			return False
			
	return False

@app.route('/GoToCreateFlights')
def GoToCreateFlights():
	if confirmstaff():
		return render_template("createflights.html")
	return redirect('/logout')



#############################
#Create New Flights
@app.route('/StaffCreate', methods = ['post'])
def StaffCreate():
	if confirmstaff():
		cursor = conn.cursor()
		query = "INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(query, (request.form['airline_name'], request.form['flight_num'], request.form['depart_date_time'], request.form['arrive_date_time'], request.form['base_price'],request.form['status'], request.form['depart_airport_code'], request.form['arrive_airport_code'], request.form['airplane_id']))
		conn.commit()
		cursor.close()
		return redirect('/StaffHome')
	else:
		return redirect('/logout') #After adding you can either logout or go home

@app.route('/ViewFlights')
def ViewFlights():
	if confirmstaff():
		return render_template("ViewFlights.html")
	return redirect('/logout')



@app.route('/StaffFlightView', methods = ['GET', 'POST'])
def StaffFlightView():
	if confirmstaff():
		cursor = conn.cursor()
		query = "SELECT * from flight where airline_name = %s AND depart_date_time >= DATE_SUB(NOW(), INTERVAL 1 MONTH);"
		cursor.execute(query, request.form['airline_name'])
		data = cursor.fetchall()
		depart = "SELECT count(c.email) as customers, p.email, t.ticket_id, p.ticket_id, t.flight_num,\
		 f.flight_num, f.depart_airport_code from customer c join ticket t join flight f \
		 join purchase p where t.ticket_id = p.ticket_id AND c.email = p.email and f.flight_num =\
		  t.flight_num and depart_airport_code = 'SFO' and f.flight_num = %s"
		cursor.execute(depart,request.form['depart_airport_code'], request.form['flight_num'])
		departing = cursor.fetchall()
		arrive = "SELECT count(c.email) as customers, p.email, t.ticket_id, p.ticket_id, t.flight_num,\
		 f.flight_num, f.arrive_airport_code from customer c join ticket t join flight f \
		 join purchase p where t.ticket_id = p.ticket_id AND c.email = p.email and f.flight_num =\
		  t.flight_num and arrive_airport_code = %s and f.flight_num = %s"
		cursor.execute(arrive, request.form['arrive_airport_code'], request.form['flight_num'])
		arrival = cursor.fetchall()
		cursor.close()
		if data:
			return render_template('ViewFlights.html', data=data)
		else:
			print("Error!")
	else:
		return redirect('/logout')

@app.route('/DepartingCustomersPointer')
def DepartingCustomerPointer():
	if confirmstaff():
		return render_template("DepartingCustomers.html")
	return redirect('/logout')

@app.route('/DepartingCustomers', methods=["get", "post"])
def DepartingCustomers():
	if confirmstaff():
		cursor = conn.cursor()
		depart = "SELECT count(c.email) as customers, p.email, t.ticket_id, p.ticket_id, t.flight_num,\
		 f.flight_num, f.depart_airport_code from customer c join ticket t join flight f \
		 join purchase p where t.ticket_id = p.ticket_id AND c.email = p.email and f.flight_num =\
		  t.flight_num and depart_airport_code = %s and f.flight_num = %s"
		cursor.execute(depart, (request.form['depart_airport_code'], request.form['flight_num']))
		departing = cursor.fetchall()
		cursor.close()
		if depart:
			return render_template('DepartingCustomers.html', departing=departing)
		else:
			print("Error!")
	else:
		return redirect('/logout')


@app.route('/ArrivingCustomersPointer')
def ArrivingCustomerPointer():
	if confirmstaff():
		return render_template("ArrivingCustomers.html")
	return redirect('/logout')

@app.route('/ArrivingCustomers', methods=["get", "post"])
def ArrivingCustomers():
	if confirmstaff():
		cursor = conn.cursor()
		arrive = "SELECT count(c.email) as customers, p.email, t.ticket_id, p.ticket_id, t.flight_num,\
		 f.flight_num, f.arrive_airport_code from customer c join ticket t join flight f \
		 join purchase p where t.ticket_id = p.ticket_id AND c.email = p.email and f.flight_num =\
		  t.flight_num and arrive_airport_code = %s and f.flight_num = %s"
		cursor.execute(arrive, (request.form['arrive_airport_code'], request.form['flight_num']))
		arriving = cursor.fetchall()
		cursor.close()
		if arrive:
			return render_template('ArrivingCustomers.html', arriving=arriving)
		else:
			print("Error!")
	else:
		return redirect('/logout')
	



@app.route('/GoToAirplane')
def GoToAirplane():
	if confirmstaff():
		return render_template("AddAirplane.html")
	return redirect('/logout')


@app.route('/AddAirplane', methods = ["GET", "POST"])
def AddAirplane():
	if confirmstaff():
		cursor = conn.cursor()
		create = "INSERT into airplane VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(create, (request.form['id'], request.form['airline_name'], request.form['num_of_seats'], request.form['manufacturing_comp'], request.form['age_of_airplane']))
		conn.commit() # python does not auto commit, therefore need to send commit after making changes 
		cursor.close()
		return redirect('/StaffHome')
	else:
		return redirect('/logout') #After adding you can either logout or go home to perform more actions.

@app.route('/GoToAirport')
def GoToAirport():
	if confirmstaff():
		return render_template("AddAirport.html")
	return redirect('/logout')


@app.route('/AddAirport', methods= ["GET", "POST"])
def AddAirport():
	if confirmstaff():
		cursor = conn.cursor()
		create = "INSERT into airport VALUES(%s, %s, %s, %s, %s)"
		cursor.execute(create, (request.form['code'], request.form['airport_name'], request.form['city'],
		request.form['country'], request.form['airport_type']))
		conn.commit() 
		cursor.close()
		return redirect("/StaffHome")
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




@app.route('/ChangeFlights')
def ChangeFlights():
	if confirmstaff():
		return render_template("ChangeFlights.html")
	return redirect('/logout')

		#############################

@app.route('/StaffChangeFlights', methods = ["GET", "POST"])
def StaffChangeFlights():
	print("Made POST Request: /StaffChangeFlights")
	print(request.form)
	if confirmstaff():
		print(request.form)
		cursor = conn.cursor()
		query =  "SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s"
		cursor.execute(query, (request.form['airline_name'], request.form['flight_num']))
		data = cursor.fetchall()
		if data:
			query = "UPDATE flight SET flight.status = %s WHERE airline_name = %s AND flight_num = %s"
			cursor.execute(query, (request.form['status'], request.form['airline_name'], request.form['flight_num']))
			conn.commit()
			cursor.close()
			print("Successful Flight Status Change!")
			return redirect('/StaffHome')
		else:
			print("Error!")
	else:
		return redirect('/logout')


########################################
@app.route('/ViewRatings')
def ViewRatings():
	if confirmstaff():
		return render_template("ViewFlightRatings.html")
	return redirect('/logout')

@app.route('/ViewFlightRatings', methods=["GET", "POST"])
def ViewFlightRatings():
	if confirmstaff():
		cursor = conn.cursor()
		average = "SELECT avg(ratings) as rating, flight_num, airline_name from rate natural \
		join flight natural join customer where airline_name = %s AND flight_num = %s;"
		cursor.execute(average, (request.form['airline_name'], request.form['flight_num']))
		data = cursor.fetchall()
		info = "select ratings, comments, airline_name, flight_num from rate natural join flight \
		natural join customer where airline_name = %s and flight_num = %s"
		cursor.execute(info, (request.form['airline_name'], request.form['flight_num']))
		information = cursor.fetchall()
		cursor.close()
		if data:
			return render_template('ViewFlightRatings.html', data=data, information = information)
		else:
			print("Error!")
	else:
		return redirect('/logout')




@app.route('/ViewEarnedRevenue', methods=["get"])
def ViewEarnedRevenue():
	if confirmstaff():
		cursor = conn.cursor()
		month = "SELECT sum(sold_price) as rev, purchase_date_time \
			     FROM purchase \
			     WHERE purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 MONTH);"
		cursor.execute(month)
		past_month = cursor.fetchall()
		year = "SELECT sum(sold_price) as rev, purchase_date_time \
			    FROM purchase \
				WHERE purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 YEAR);"
		cursor.execute(year)
		past_year = cursor.fetchall()
		cursor.close()

		return render_template('ViewEarnedRevenue.html', past_month = past_month, past_year = past_year)
	else:
		return redirect('/logout')
'''
@app.route('/ViewFrequentCustomers', methods=["get"])
def ViewFrequentCustomers():
	if confirmstaff():
		f
'''
@app.route('/ViewTopDestinations', methods=["get"])
def ViewTopDestinations():
	if confirmstaff():
		cursor = conn.cursor()
		month = "SELECT arrive_airport_code, count(t.ticket_id) FROM flight f JOIN ticket t ON f.flight_num = t.flight_num  \
                JOIN purchase p ON t.ticket_id = p.ticket_id AND p.purchase_date_time >= DATE_SUB(NOW(), INTERVAL 3 MONTH)  \
                GROUP BY arrive_airport_code ORDER BY count(t.ticket_id) DESC LIMIT 3"
		cursor.execute(month)
		past_three_months = cursor.fetchall()
		year = "SELECT arrive_airport_code, count(t.ticket_id) FROM flight f JOIN ticket t ON f.flight_num = t.flight_num \
                JOIN purchase p ON t.ticket_id = p.ticket_id AND p.purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 year)  \
                GROUP BY arrive_airport_code ORDER BY count(t.ticket_id) DESC LIMIT 3"
		cursor.execute(year)
		past_year = cursor.fetchall()
		cursor.close()
		return render_template('ViewTopDestinations.html', past_three_months = past_three_months, past_year = past_year)
	else:
		return redirect('/logout')

@app.route('/ViewRevByTravelClassPoint')
def ViewRevByTravelClassPoint():
	if confirmstaff():
		return render_template("TravelClass.html")
	return redirect('/logout')


@app.route('/ViewRevByTravelClass', methods=["get", "post"])
def ViewReportsByTravelClass():
	if confirmstaff():
		cursor = conn.cursor()
		travel =  "SELECT sum(sold_price) as rev, travel_class FROM purchase join \
		ticket where travel_class = %s;"
		cursor.execute(travel, request.form['travel_class'])
		revenue = cursor.fetchall()
		if revenue:
			return render_template('TravelClass.html', revenue=revenue)
		else:
			print("Error!")
	else:
		return redirect('/logout')

		

@app.route('/ViewReports', methods=["get"])
def	ViewReports():
	if confirmstaff():
		cursor = conn.cursor()
		month = "select count(t.ticket_id) from ticket t ,purchase p \
		where t.ticket_id = p.ticket_id AND \
		purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 MONTH);"
		cursor.execute(month)
		past_month = cursor.fetchall()
		year = "select count(t.ticket_id) from ticket t ,purchase p \
		where t.ticket_id = p.ticket_id AND \
		purchase_date_time >= DATE_SUB(NOW(), INTERVAL 1 year);"
		cursor.execute(year)
		past_year = cursor.fetchall()
		cursor.close()
		return render_template('ViewReports.html', past_month = past_month, past_year = past_year)
	else:
		return redirect('/logout')

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
