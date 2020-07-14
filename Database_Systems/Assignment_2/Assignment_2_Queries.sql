USE Assignment2;
#1
##e
###a
SELECT 
    instName
FROM
    Instructor
WHERE
    sessional = TRUE;
###b
SELECT 
    Instructor.instName
FROM
    Instructor
        INNER JOIN
    Offering ON Instructor.instID = Offering.instID
WHERE
    yearCode > minTempVal
        AND yearCode < maxTempVal; #minTempVal and maxTempVal are the year values that you want to analyze

#--------------------------------------------------------------------------------------------------------------

###c
SELECT 
    COUNT(instName)
FROM
    (SELECT 
        Instructor.instName
    FROM
        Instructor
    INNER JOIN Offering ON Instructor.instID = Offering.instID
    WHERE
        sessional = TRUE) AS CoursesTaughtBySessionals;
        
#--------------------------------------------------------------------------------------------------------------

###d
SELECT 
    SUM(enrollment)
FROM
    (SELECT 
        Offering.enrollment
    FROM
        Instructor
    INNER JOIN Offering ON Instructor.instID = Offering.instID
    WHERE
        sessional = TRUE) AS StudentsTaughtBySessionals;
        
#--------------------------------------------------------------------------------------------------------------

###e
SELECT 
    COUNT(instName)
FROM
    Instructor
        INNER JOIN
    Department ON Instructor.deptID = Department.deptID
WHERE
    sessional = TRUE
GROUP BY faculty;

#-----------------------------------------------------------------------------------------------------------------------------------------

#use Assignment2;
/*
#Creating index
CREATE INDEX idx_pname
ON Persons (LastName, FirstName);

#Deleting indices
Alter table Persons
drop index idx_pname;
*/

#
##f
###a
/*
For the first query a covering index of sessional with instructor would help by making the db engine
work through the table instead of using the where
*/
create index ind_sessionalInstructor
on Instructor (sessional, instName);

/*
Alter table Instructor
drop index ind_sessionalInstructor;
*/

explain SELECT 
    instName
FROM
    Instructor
WHERE
    sessional = TRUE;
    
###b
#ind_sessionalInstructor also works for the first part of the second query
#For the second part the explain mentions that a possible key would be related to the term code

Explain SELECT 
    Instructor.instName
FROM
    Instructor
        INNER JOIN
    Offering ON Instructor.instID = Offering.instID
WHERE
    yearCode > 2017 #minTempVal
        AND yearCode < 2020; #maxTempVal. Both minTempVal and maxTempVal are the term values that you want to analyze

show index from Offering;
###c
explain SELECT 
    COUNT(instName)
FROM
    (SELECT 
        Instructor.instName
    FROM
        Instructor
    INNER JOIN Offering ON Instructor.instID = Offering.instID
    WHERE
        sessional = TRUE) AS CoursesTaughtBySessionals;
        
###d
explain SELECT 
    SUM(enrollment)
FROM
    (SELECT 
        Offering.enrollment
    FROM
        Instructor
    INNER JOIN Offering ON Instructor.instID = Offering.instID
    WHERE
        sessional = TRUE) AS StudentsTaughtBySessionals;
###e
SELECT 
    COUNT(instName)
FROM
    Instructor
        INNER JOIN
    Department ON Instructor.deptID = Department.deptID
WHERE
    sessional = TRUE
GROUP BY faculty;


##f
/*
Using the original tables (without the modifications asked in 1.d.), it can be seen that running
*/
explain select count(courseID) from Course inner join Department using (deptID) where prereqID is NULL and faculty=’Math’;
