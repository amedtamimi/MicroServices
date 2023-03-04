CREATE DATABASE db;

USE db;

CREATE TABLE grades (
    id INT NOT NULL AUTO_INCREMENT,
    student_name VARCHAR(50) NOT NULL,
    course VARCHAR(50) NOT NULL,
    grade INT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO grades (student_name, course, grade, date) values ('John', 'Math', 90, '2015-01-01');
INSERT INTO grades (student_name, course, grade, date) values ('John', 'English', 80, '2015-01-01');
