insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("jaeha@gmail.com","ohhey1", "Jaeha Huh", 5, "Metrotech", "Brooklyn", "NY", "6469991111", 111, '2025-12-31', "South Korea", '1995-09-21');
insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("nacho@gmail.com", "ohhey2", "Nacho lee", 5, "Metrotech", "Brooklyn", "NY", "6468881111", 222, '2024-12-05', "United States", '1999-04-15');    
insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("hunni@gmail.com", "ohhey3", "hunni ho", 5, "Metrotech", "Brooklyn", "NY", "6467773333", 333, '2024-11-10', "United States", '2000-12-30');

insert into airport (code, airport_name, city, country, airport_type) values ("AAA", "PVG", "Shanghai", "China", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("ZZZ", "JFK", "NYC", "USA", "both");


insert into airline (airline_name) values ("China Eastern");


insert into airline_staff (username, airline_name, password, first_name, last_name, date_of_birth) values ("CJ@gmail.com", "China Eastern", "heycj", "CJ", "Nnorom", '2000-10-30');


insert into staff_phone_num (username, phone_num) values ("CJ@gmail.com", "6467175333");
insert into staff_phone_num (username, phone_num) values ("CJ@gmail.com", "6467175555");
insert into staff_phone_num (username, phone_num) values ("CJ@gmail.com", "6467175111");


insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("Boeing 737-800", "China Eastern", 200, "Boeing", 10);
insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("Boeing 737-700",  "China Eastern", 150, "Boeing", 8);
insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("Boeing 747-400",  "China Eastern", 220, "Boeing", 5);




insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code) values ("China Eastern", 001, "2022-05-05 15:15:00",  '2022-05-06 01:00:00', 1000, "ontime", "AAA", "ZZZ");
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code) values ("China Eastern", 002, '2022-09-11 20:20:00', '2022-09-12 04:00:00', 1050, "delayed", "ZZZ", "AAA");
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code) values ("China Eastern", 003, '2022-07-05 09:30:00', '2021-07-05 23:00:00', 1200, "ontime", "AAA", "ZZZ");




insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, sold_price) values (100, "China Eastern",  001, "2022-05-05 15:15:00", 1000);
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, sold_price) values (200, "China Eastern",  001, "2022-05-05 15:15:00", 1100);
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, sold_price) values (300, "China Eastern", 002, '2022-09-11 20:20:00', 1050);
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, sold_price) values (400, "China Eastern", 002, '2022-09-11 20:20:00', 900);
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, sold_price) values (500, "China Eastern", 003, '2022-07-05 09:30:00', 1200);



insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time) 
values ("jaeha@gmail.com", 100, "credit", 12345, "Jaeha Huh", '2024-09-01', '2022-01-10 11:00:00');

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time ) 
values ("hunni@gmail.com", 200, "credit", 12555, "hunni ho", '2024-10-01', '2022-01-11 14:00:00');

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time) 
values ("nacho@gmail.com", 300, "debit", 39998, "nacho lee", '2024-01-01', '2022-02-02 18:00:00');

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time ) 
values ("jaeha@gmail.com", 400, "credit", 12345, "Jaeha Huh", '2024-09-01', '2022-02-15 12:00:00');

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time) 
values ("nacho@gmail.com", 500, "credit", 39998,"nacho lee", '2024-10-01', '2022-01-10 14:00:00');


