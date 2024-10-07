CREATE TABLE members (
    -- Primary key means unique and not null
    id SERIAL PRIMARY KEY, fname VARCHAR(35), lname VARCHAR(35)
);

CREATE TABLE users (
    username VARCHAR(35) PRIMARY KEY,
    password TEXT NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE classes (
    name VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE enrollments (
    class VARCHAR(50) REFERENCES classes (name),
    username VARCHAR(35) REFERENCES users (username),
    PRIMARY KEY (class, username)
);

-- Might need a comments table?
