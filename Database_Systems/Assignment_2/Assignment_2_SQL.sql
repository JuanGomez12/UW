/*
USE Assignment2;

#1
##d
#Turn off foreign key check
SET foreign_key_checks = 0;

drop table if exists Offering;
drop table if exists Instructor;
drop table if exists Course;
drop table if exists CoursePrereq;
drop table if exists Classroom;
drop table if exists Department;

#Turn back on foreign key check
SET foreign_key_checks = 1;

create table Classroom (
roomID char(8) PRIMARY KEY,
Building char(4),
Room decimal(4),
Capacity int);

insert into Classroom
values ('E74417', 'E7', 4417, 138),
		('E74053', 'E7', 4053 , 144 ),
		('RCH111' , 'RCH' , 111 , 91 ),
		('RCH101' , 'RCH', 101 , 250 );


create table Department (
deptID char(8) PRIMARY KEY,
deptName varchar(50),
faculty varchar(50));
insert into Department
values ('ECE' , 'Electrical and Computer Engineering' , 'Engineering' ),
		('CS'  , 'Computer Science' , 'Math' ),
		('MATH'  , 'Math' , 'Math' ),
		('C&O'  , 'Combinatorics and Optimization' , 'Math' );

#we need to add the deptID foreign key
create table Instructor(
instID int PRIMARY KEY,
instName char(10),
deptID char(4),
sessional bool,
FOREIGN KEY (deptID) REFERENCES Department(deptID));
insert into Instructor values (1 , 'Nelson' , 'ECE' , false ),
       	    	       	      (3 , 'Jimbo'  , 'ECE' , false ),
			      (4 , 'Moe'    , 'CS'  , true ),
			      (5 , 'Lenny'  , 'CS'  , false );

create table Course (
courseID char(8) PRIMARY KEY,
courseName varchar(50),
deptID char(4),
FOREIGN KEY (deptID) REFERENCES Department(deptID));
insert into Course
values ('ECE356'  , 'Database Systems' , 'ECE'),
		('ECE358'  , 'Computer Networks' , 'ECE'),
		('ECE390'  , 'Engineering Design' , 'ECE'),
		('MATH117' , 'Calculus 1'  , 'MATH');

#We must create the prereq table, with foreign keys to courseID
#Turn off foreign key check
SET foreign_key_checks = 0;
              
CREATE TABLE CoursePrereq (
courseID char(8),
prereqID char(8),
PRIMARY KEY(courseID, prereqID),
FOREIGN KEY (courseID) REFERENCES Course(courseID),
FOREIGN KEY (prereqID) REFERENCES Course(courseID));

insert into CoursePrereq
values ('ECE356'  , 'ECE250' ),
		('ECE358'  , 'ECE222' ),
		('ECE390'  , 'ECE290' );
              
#Turn back on foreign key check
SET foreign_key_checks = 1;
        
#Create the offering table, with foreign keys to Classroom.roomID, Course.courseID and Seasons.termCode
create table Offering (
courseID char(8),
section int,
yearCode decimal(4),
termCode decimal(1),
roomID char(8),
instID int,
enrollment int,
PRIMARY KEY (courseID, section, yearCode, termCode),
FOREIGN KEY (roomID) REFERENCES Classroom(roomID),
FOREIGN KEY (courseID) REFERENCES Course(courseID));
insert into Offering 
values ('ECE356'  , 1, 2019, 1 , 'E74417' , 1 , 64 ),
		('ECE356'  , 2, 2019, 1 , 'E74417' , 3 , 123 ),
		('ECE358'  , 2, 2019, 1 , 'E74417' , 1 , 123 ),
		('ECE390'  , 1, 2019, 1 , 'E74053' , 1 , 102 ),
		('MATH117' , 1, 2018, 9 , 'E74043' , 5 , 134 );
*/
        

USE Assignment2;

#1
##d
#Turn off foreign key check
SET foreign_key_checks = 0;

drop table if exists Offering;
drop table if exists Instructor;
drop table if exists Course;
drop table if exists CoursePrereq;
drop table if exists Classroom;
drop table if exists Department;

#Turn back on foreign key check
SET foreign_key_checks = 1;

create table Classroom (
roomID char(8) PRIMARY KEY,
Building char(4),
Room decimal(4),
Capacity int);
#Run Classroom_Table.sql
#SOURCE Classroom_Table.sql

create table Department (
deptID char(8) PRIMARY KEY,
deptName varchar(50),
faculty varchar(50));
#Run Department_Table
#SOURCE Department_Table.sql

#we need to add the deptID foreign key
create table Instructor(
instID int PRIMARY KEY,
instName char(15),
deptID char(4),
sessional bool,
FOREIGN KEY (deptID) REFERENCES Department(deptID));
#Run Instructor_table.sql
#SOURCE Instructor_Table.sql

create table Course (
courseID char(8) PRIMARY KEY,
courseName varchar(70),
deptID char(4),
FOREIGN KEY (deptID) REFERENCES Department(deptID));
#Run Course_Table.sql
#SOURCE Course_Table.sql

#We must create the prereq table, with foreign keys to courseID
#Turn off foreign key check
SET foreign_key_checks = 0;
              
CREATE TABLE CoursePrereq (
courseID char(8),
prereqID char(8),
PRIMARY KEY(courseID, prereqID),
FOREIGN KEY (courseID) REFERENCES Course(courseID),
FOREIGN KEY (prereqID) REFERENCES Course(courseID));
#Run Prerequisites_Table.sql
#SOURCE Prerequisites_Table.sql

#Turn back on foreign key check
SET foreign_key_checks = 1;

#Create the offering table, with foreign keys to Classroom.roomID, Course.courseID and Seasons.termCode
create table Offering (
courseID char(8),
section int,
yearCode decimal(4),
termCode decimal(1),
roomID char(8),
instID int,
enrollment int,
PRIMARY KEY (courseID, section, yearCode, termCode),
FOREIGN KEY (roomID) REFERENCES Classroom(roomID),
FOREIGN KEY (courseID) REFERENCES Course(courseID));
#Run Offering_Table.sql
#SOURCE Offering_Table.sql;

