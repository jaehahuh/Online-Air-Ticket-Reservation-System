create table customer (
	email		varchar(100),
	password		varchar(200),
	name		varchar(100),
	addr_building_num	int,
	addr_street		varchar(100),
	addr_city		varchar(100),
	addr_state		varchar(100),
	phone_num	varchar(100),
	passport_num	int,
	passport_exp	date,
	passport_country	varchar(100),
	date_of_birth	date,
	primary key (email)	
);


create table airport (
	code		varchar(100),
	airport_name	varchar(100),
	city		varchar(100),
	country		varchar(100),
	airport_type	varchar(100),
	primary key (code)
);


create table airline (
    	airline_name	varchar(100),
	primary key (airline_name)
);

create table airline_staff (
	username		varchar(100), 
	airline_name	varchar(100),
	password		varchar(200),
	first_name		varchar(100),
	last_name 		varchar(100),
	date_of_birth	date,
	primary key (username, airline_name),
	foreign key (airline_name) references airline(airline_name) on delete cascade
);

create table staff_phone_num(
	username		varchar(100),
	phone_num 	varchar(100),
	primary key (phone_num),
    	foreign key (username) references airline_staff(username) on delete cascade
);


create table airplane (
	id		varchar(100),
	airline_name	varchar(100),
	num_of_seats	int,
	manufacturing_comp	varchar(100),
	age_of_airplane	int,
	primary key (id),
	foreign key (airline_name) references airline(airline_name) on delete cascade
);



create table flight (
	airline_name	varchar(100),
	flight_num		int,
    	depart_date_time	datetime,
    	arrive_date_time	datetime,
   	base_price 	int,
    	status		varchar(100),
	depart_airport_code	varchar(100),
	arrive_airport_code	varchar(100),
	primary key (airline_name, flight_num, depart_date_time),
	foreign key (depart_airport_code) references airport(code) on delete set null,
	foreign key (arrive_airport_code) references airport(code) on delete set null,
	foreign key (airline_name) references airline(airline_name) on delete cascade
);


create table ticket (
	ticket_id		int,
	airline_name	varchar(100),
	flight_num		int,	
	depart_date_time	datetime,
	sold_price		int,
	primary key (ticket_id),
	foreign key (airline_name, flight_num, depart_date_time) references flight(airline_name, flight_num, depart_date_time) on delete cascade
);


create table purchase (
	email		varchar(100),
	ticket_id		int,
	card_num 		int,
	card_type 		varchar(100),
   	card_name		varchar(100),
    	card_exp		date,
	purchase_date_time 	datetime,
	primary key (email, ticket_id),
	foreign key (email) references customer (email) on delete cascade,
	foreign key (ticket_id) references ticket (ticket_id) on delete cascade
);


create table rate (
	email 		varchar(100),
	airline_name	varchar(100),
    	flight_num		int,
	depart_date_time	datetime,
   	ratings 		int,
	comments 		varchar(500),
 	primary key (email,  airline_name, flight_num, depart_date_time),
	foreign key (email) references customer (email) on delete cascade,
	foreign key (airline_name, flight_num, depart_date_time) references flight (airline_name, flight_num, depart_date_time) on delete cascade
);






