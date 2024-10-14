CREATE TABLE members (
    -- Primary key means unique and not null
    id SERIAL PRIMARY KEY,
    fname VARCHAR(35),
    lname VARCHAR(35),
    email VARCHAR(254)
);

CREATE TABLE users (
    username VARCHAR(35) PRIMARY KEY,
    password TEXT NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    member_id INTEGER REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE classes (
    name VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE comments (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    classname VARCHAR(50) REFERENCES classes (name) ON DELETE CASCADE,
    username VARCHAR(35) REFERENCES users (username) ON DELETE CASCADE,
    comment TEXT NOT NULL
);

CREATE TABLE enrollments (
    class VARCHAR(50) REFERENCES classes (name) ON DELETE CASCADE,
    username VARCHAR(35) REFERENCES users (username) ON DELETE CASCADE,
    PRIMARY KEY (class, username)
);
