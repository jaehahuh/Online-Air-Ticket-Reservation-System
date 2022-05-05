#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airport',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

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



#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']
    user_type= request.form['user_type']
    cursor = conn.cursor()
    
    #check info from the database
    if (user_type == 'custo'):
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, (username))
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
        inst = 'INSERT into customer values(%s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(inst, (username, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth))

    
    elif (user_type == 'staff'):
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
        error = None
        
        if(data):
            #if staff is already exist in data
            error = "Already a registered user."
            return render_template('register.html', error = error)

        #if new staff
        
        airline_name = request.form['airline_name']
        query = 'SELECT * FROM airline WHERE name = %s'
        cursor.execute(query, (airline_name))
        
        if not cursor.fetchone():
            error = "This airline does not exists"
            return render_template('register.html', error = error)
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        phone_nums = request.form['phone_nums'].split(', ')
        
        inst  = 'INSERT into airline_staff values (%s, md5(%s), %s, %s, %s)'
        cursor.execute(inst, (username, password, first_name, last_name, date_of_birth))

        for number in phone_nums:
            ins  = 'INSERT into staff_phone_num values (%s, %s)'
            cursor.execute(inst, (username, number))
            
    conn.commit()
    cursor.close()
    
    return render_template('index.html')


#View public info
@app.route('/public_view_info', methods=['GET', 'POST'])
def searchPublicView():
    cursor = conn.cursor()
    dept = request.form['depart']
    arri = request.form['arrive']
    depart_date = request.form['depart_date']
    query = 'SELECT distinct f.airline_name, f.flight_num, de.airport_name as depart_airport, depart_date_time, ar.airport_name as arrive_airport, arrive_date_time, f.status '
    query +='FROM flight f, airport de, airport ar'
    query +='WHERE ((f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND  ("{}" = de.city or "{}" = de.airport_name)'.format(dept, dept)
    query +='AND "{}" = ar.city or "{}" = ar.airport_name)'.format(arri, arri)
    query +='AND ("{}" = date(f.depart_date_time))'.format(depart_date)
    query +='ORDER BY f.depart_date_time)'
    if "return_date" in request.form:
        return_date = request.form['return_date']
        query += 'OR ((f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND ("{}" = de.city or "{}" = de.airport_name)'.format(dept, dept)
        query += ' AND "{}" = ar.city or "{}" = ar.airport_name)'.format(arri, arri)
        query += 'AND ("{}" = date(f.depart_date_time))'.format(return_date)
        query += 'ORDER BY f.depart_date_time)'
    cursor.execute(query)
    conn.commit()
    data1 = cursor.fetchall()

    cursor.close()
    return render_template('home.html', public_flight_info=data1)


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
    username = session['username']
    dept = request.form['depart']
    arri = request.form['arrive']
    depart_date = request.form['depart_date']
    query = 'SELECT distinct f.airline_name, f.flight_num, de.airport_name as depart_airport, depart_date_time, ar.airport_name as arrive_airport, arrive_date_time, f.base_price'
    query += 'FROM flight f, airport de, airport ar'
    query += 'WHERE ((f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND  ("{}" = de.city or "{}" = de.airport_name)'.format(dept, dept)
    query += ' AND "{}" = ar.city or "{}" = ar.airport_name)'.format(arri, arri)
    query += 'AND ("{}" = date(f.depart_date_time))'.format(depart_date)
    query += 'ORDER BY f.depart_date_time)'
    if "return_date" in request.form:
        return_date = request.form['return_date']
        query += 'OR ((f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND ("{}" = de.city or "{}" = de.airport_name)'.format(dept, dept)
        query += ' AND "{}" = ar.city or "{}" = ar.airport_name)'.format(arri, arri)
        query += 'AND ("{}" = date(f.depart_date_time))'.format(return_date)
        query += 'ORDER BY f.depart_date_time)'
    cursor.execute(query)
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
    print(exist1)
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
@app.route('/history')
def history():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT sum(sold_price)  FROM ticket Natural JOIN purchase WHERE email = %s and purchase_date_time between date_sub(now(), interval 1 year)'
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
        query = 'SELECT sum(sold_price) FROM ticket Natural JOIN purchase where email = %s and monthname(purchase_date_time) = %s'
        cursor.execute(query, (username, month))
        total_spent_month = cursor.fetchone()
        total_spent_month = total_spent_month.get('sum(sold_price)')
        if total_spent_month:
            past_six_month[month] = total_spent_month

    #History of Past flights
    query = 'SELECT DISTINCT f.airline_name, f.flight_num, de.airport_name as depart_airport, f.depart_date_time, ar.airport_name as arrive_airport, f.arrive_date_time'
    query += 'FROM flight f, airport de, airport ar, (purchase p NATURAL JOIN ticket t)'
    query += 'WHERE (f.depart_airport_code = de.code AND f.arrive_airport_code = ar.code) AND p.ticket_id = t.ticket_id AND t.flight_num = f.flight_num AND p.email = %s'
    query += 'ORDER BY f.depart_date_time'
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
    
    query = 'SELECT date(purchase_date_time), ticket_id, sold_price as sale_price From ticket NATURAL JOIN purchase'
    query += 'WHERE email = %s and date(purchase_date_time) between date(%s) and date(%s)'
    cursor.execute(query, (username, start_date, end_date))
    history_date = cursor.fetchall()
    for line in history_date:
        print(line)
    return render_template('custo_history.html', total_spent_interval=total_spent, start_month=start_month, end_month=end_month, history_date=history_date)





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
