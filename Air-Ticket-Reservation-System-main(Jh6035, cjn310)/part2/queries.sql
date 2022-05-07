1. select * from flight where depart_date_time > now();

2. select * from flight where status = 'delayed';

3. select distinct c.name from customer c, purchase p where p.email = c.email;

4. select distinct id from airplane where airline_name = 'China Eastern';
