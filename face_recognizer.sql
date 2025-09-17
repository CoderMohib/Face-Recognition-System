create database face_recognizer;
use face_recognizer;
CREATE TABLE student (
    DEP VARCHAR(45),
    Course VARCHAR(45),
    Year VARCHAR(45),
    Semester VARCHAR(45),
    StudentID INT PRIMARY KEY,
    Name VARCHAR(45),
    Divison VARCHAR(45),
    Roll VARCHAR(45),
    Gender VARCHAR(45),
    DOB VARCHAR(45),
    Email VARCHAR(45),
    Phone VARCHAR(45),
    Address VARCHAR(45),
    Teacher VARCHAR(45),
    PhotoSample VARCHAR(45)
);

CREATE TABLE register (
    f_name VARCHAR(45),
    l_name VARCHAR(45),
    contact VARCHAR(45),
    email VARCHAR(45) PRIMARY KEY,
    securityQ VARCHAR(45),
    securityA VARCHAR(45),
    password VARCHAR(45)
);

