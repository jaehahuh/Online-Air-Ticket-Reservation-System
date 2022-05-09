insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("testcustomer@nyu.edu","1234", "Test Customer 1", 1555, "Jay St", "Brooklyn", "New York", "123-4321-4321", 54321, '2025-12-24', "USA", '1999-12-19');
insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("user1@nyu.edu","1234", "User1", 5405, "Jay Street", "Brooklyn", "New York", "123-4322-4322", 54322, '2025-12-25', "USA", '1999-11-19');
insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("user2@nyu.edu","1234", "User2", 1702, "Jay Street", "Brooklyn", "New York", "123-4323-4323", 54323, '2025-10-24', "USA", '1999-10-19');
insert into customer (email, password, name, addr_building_num, addr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("user3@nyu.edu","1234", "User3", 1890, "Jay Street", "Brooklyn", "New York", "123-4324-4324", 54324, '2025-09-24', "USA", '1999-09-19');


insert into airport (code, airport_name, city, country, airport_type) values ("JFK", "JFK", "NYC", "USA", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("BOS", "BOS", "NYC", "USA", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("PVG", "PVG", "Shanghai", "China", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("BEI", "BEI", "Beijing", "China", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("SFO", "SFO", "San Francisco", "USA", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("LAX", "LAX", "Los Angeles", "USA", "both");
insert into airport (code, airport_name, city, country, airport_type) values ("HKA", "HKA", "Hong Kong", "China", "both");


insert into airline (airline_name) values ("Delta");


insert into airline_staff (username, airline_name, password, first_name, last_name, date_of_birth) values ("admin", "Delta", "abcd", "Roe", "Jones", '1978-05-25');



insert into staff_phone_num (username, phone_num) values ("admin", "111-2222-3333");
insert into staff_phone_num (username, phone_num) values ("admin", "444-5555-6666");



insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("1", "Delta", 4, "Boeing", 10);
insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("2",  "Delta", 4, "Airbus", 12);
insert into airplane (id, airline_name, num_of_seats, manufacturing_comp, age_of_airplane) values ("3",  "Delta", 50, "Boeing", 8);





insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 102, "2022-04-12 13:25:25",  '2022-04-12 16:50:25', 300, "on-time", "SFO", "LAX", 3);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 104, "2022-05-06 13:25:25",  '2022-05-06 16:50:25', 300, "on-time", "PVG", "BEI", 3);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 106, "2022-03-04 13:25:25",  '2022-03-04 16:50:25', 350, "delayed", "SFO", "LAX", 3);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 206, "2022-06-04 13:25:25",  '2022-06-04 16:50:25', 400, "on-time", "SFO", "LAX", 2);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 207, "2022-07-04 13:25:25",  '2022-07-04 16:50:25', 300, "on-time", "SFO", "LAX", 2);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 134, "2022-02-12 13:25:25",  '2022-02-12 16:50:25', 300, "delayed", "JFK", "BOS", 3);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 296, "2022-06-01 13:25:25",  '2022-06-01 16:50:25', 3000, "on-time", "PVG", "SFO", 1);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 715, "2022-04-28 10:25:25",  '2022-04-28 13:50:25', 500, "delayed", "PVG", "BEI", 1);
insert into flight (airline_name, flight_num, depart_date_time, arrive_date_time, base_price, status, depart_airport_code, arrive_airport_code, airplane_id) values 
("Delta", 839, "2022-07-12 13:25:25",  '2022-07-12 16:50:25', 800, "on-time", "PVG", "BOS", 3);




insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (1, "Delta",  102, "2022-04-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (2, "Delta",  102, "2022-04-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (3, "Delta",  102, "2022-04-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (4, "Delta",  104, "2022-05-06 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (5, "Delta",  104, "2022-05-06 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (6, "Delta",  106, "2022-03-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (7, "Delta",  106, "2022-03-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (8, "Delta",  839, "2022-07-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (9, "Delta",  102, "2022-04-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (11, "Delta",  134, "2022-02-12 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (12, "Delta",  715, "2022-04-28 10:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (14, "Delta",  206, "2022-06-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (15, "Delta",  206, "2022-06-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (16, "Delta",  206, "2022-06-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (17, "Delta",  207, "2022-07-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (18, "Delta",  207, "2022-07-04 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (19, "Delta",  296, "2022-06-01 13:25:25", "Economy");
insert into ticket (ticket_id, airline_name, flight_num, depart_date_time, travel_class) values (20, "Delta",  296, "2022-06-01 13:25:25", "Economy");



insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 1, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-03-04 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user1@nyu.edu", 2, "credit", "1111-2222-3333-5555", "User 1", '03/2023', '2022-03-03 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user2@nyu.edu", 3, "credit", "1111-2222-3333-5555", "User 2", '03/2023', '2022-04-04 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user1@nyu.edu", 4, "credit", "1111-2222-3333-5555", "User 1", '03/2023', '2022-03-21 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 5, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-04-28 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 6, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-03-05 11:55:55', 350);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user3@nyu.edu", 7, "credit", "1111-2222-3333-5555", "User 3", '03/2023', '2022-02-03 11:55:55', 350);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user3@nyu.edu", 8, "credit", "1111-2222-3333-5555",  "User 3", '03/2023', '2022-07-03 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user3@nyu.edu", 9, "credit", "1111-2222-3333-5555", "User 3", '03/2023', '2022-02-04 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user3@nyu.edu", 11, "credit", "1111-2222-3333-5555", "User 3", '03/2023', '2022-07-23 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 12, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-03-02 11:55:55', 500);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user3@nyu.edu", 14, "credit", "1111-2222-3333-5555", "User 3", '03/2023', '2022-05-05 11:55:55', 400);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user1@nyu.edu", 15, "credit", "1111-2222-3333-5555", "User 1", '03/2023', '2022-05-06 11:55:55', 400);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user2@nyu.edu", 16, "credit", "1111-2222-3333-5555", "User 2", '03/2023', '2022-04-19 11:55:55', 400);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user1@nyu.edu", 17, "credit", "1111-2222-3333-5555", "User 1", '03/2023', '2022-03-11 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 18, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-04-25 11:55:55', 300);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("user1@nyu.edu", 19, "credit", "1111-2222-3333-5555", "User 1", '03/2023', '2022-05-04 11:55:55', 3000);
insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time , sold_price ) 
values ("testcustomer@nyu.edu", 20, "credit", "1111-2222-3333-4444", "Test Customer 1", '03/2023', '2022-02-12 11:55:55', 3000);





insert into rate (email, airline_name, flight_num, depart_date_time, ratings, comments) values ("testcustomer@nyu.edu", "Delta", 102, '2022-04-12 13:25:25', 4, "Very Comfortable");

insert into rate (email, airline_name, flight_num, depart_date_time, ratings, comments) values ("user1@nyu.edu", "Delta", 102, '2022-04-12 13:25:25', 5, "Relaxing, check-in and onboarding very professional");

insert into rate (email, airline_name, flight_num, depart_date_time, ratings, comments) values ("user2@nyu.edu", "Delta", 102, '2022-04-12 13:25:25', 3, "Satisfied and will use the same flight again");

insert into rate (email, airline_name, flight_num, depart_date_time, ratings, comments) values ("testcustomer@nyu.edu", "Delta", 104, '2022-05-06 13:25:25', 1, "Customer Care services are not good" );

insert into rate (email, airline_name, flight_num, depart_date_time, ratings, comments) values ("user1@nyu.edu", "Delta", 104, '2022-05-06 13:25:25', 5,  "Comfortable journey and Professional");

