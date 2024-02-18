/* PostgreSQL */

CREATE DATABASE example;

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age SMALLINT NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    isbn VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    cant_pages INTEGER,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER,
    CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

INSERT INTO authors (name, age) VALUES ('Diego', 29);
INSERT INTO books (isbn, name, cant_pages, author_id) VALUES 
('10-000-0000-00-0','Book 1', 100, 1),
('20-000-0000-00-0','Book 2', 200, 1),
('30-000-0000-00-0','Book 3', 300, 1);