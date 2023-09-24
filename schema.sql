CREATE TABLE items (id SERIAL PRIMARY KEY, name TEXT, price NUMERIC(7,2), category TEXT, 
time DATE, sold INT, grades NUMERIC(3,2));
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, admin BOOLEAN DEFAULT FALSE); 
