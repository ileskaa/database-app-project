CREATE TABLE members (
    id SERIAL PRIMARY KEY, fname VARCHAR(35), lname VARCHAR(35)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY, username VARCHAR(35), password TEXT, admin BOOLEAN
);

CREATE TABLE classes (
CREATE TABLE enrollments (
    class VARCHAR(50) REFERENCES classes (name),
    username VARCHAR(35) REFERENCES users (username),
    PRIMARY KEY (class, username)
);
