CREATE TABLE members (
    id SERIAL PRIMARY KEY, fname VARCHAR(35), lname VARCHAR(35)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY, username VARCHAR(35), password TEXT, admin BOOLEAN
);

CREATE TABLE classes (
    name VARCHAR(50) UNIQUE,
    description TEXT
);
