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
    termCode > minTempVal
        AND termCode < maxTempVal; #minTempVal and maxTempVal are the term values that you want to analyze
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
###e
SELECT 
    COUNT(instName)
FROM
    Instructor
        INNER JOIN
    Department ON Instructor.deptID = Department.deptID
WHERE
    sessional = TRUE
GROUP BY faculty

