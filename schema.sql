CREATE TABLE items (id SERIAL PRIMARY KEY, name TEXT, price NUMERIC(7,2), category TEXT, 
time DATE, sold INT, grades NUMERIC(3,2));
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, admin BOOLEAN DEFAULT FALSE); 
CREATE TABLE bought (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), item_id INT REFERENCES items(id), quantity INT, time DATE);
CREATE TABLE cart (id SERIAL PRIMARY KEY, item_id INT REFERENCES items(id), quantity INT, user_id INT REFERENCES users(id));
CREATE TABLE reviews (id SERIAL PRIMARY KEY, item_id INT REFERENCES items(id), user_id INT REFERENCES users(id), content TEXT, grade INT);