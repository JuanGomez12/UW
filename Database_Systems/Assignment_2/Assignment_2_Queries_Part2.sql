/*
ECE 656
Assignment 2, Part 2
Juan Manuel Gomez Gonzalez
UW ID:20805369
*/

set profiling=1; #Capture profile information of queries
show profiles; #show query time
show profile for query 1; #Shows info related to the query execution

/*
#Delete and reset user profiles
SET @@profiling = 0;
SET @@profiling_history_size = 0;
SET @@profiling_history_size = 100; 
SET @@profiling = 1;
*/

/*
#Creating index
CREATE INDEX idx_pname
ON Persons (LastName, FirstName);

#Deleting indices
Alter table Persons
drop index idx_pname;
*/

#2
#(a)
explain
SELECT COUNT(bDay.playerID) AS missingBDay
FROM(
	SELECT playerID, birthYear, birthMonth, birthDay
	FROM Master
	WHERE birthYear=0
	OR birthMonth=0
	OR birthday=0) AS bDay;


#(b)
#explain
SELECT SUM(IF(deadOrAlive.avgDeath> 0, -1, 1)) AS aliveMinusDeadPlayers
FROM(
	SELECT HOF.playerID, avg(M.deathYear) as avgDeath
	FROM HallOfFame HOF
	LEFT JOIN Master M
	ON HOF.playerID = M.playerID
	GROUP BY HOF.playerID) as deadOrAlive;
    
#c
#explain
/*
#Creating index
CREATE INDEX idx_salary
ON Salaries (salary);

#Deleting indices
Alter table Persons
drop index idx_pname;
*/

Alter table Salaries
drop index idx_salary;

explain
SELECT S.playerID, nameFirst, nameLast, SUM(salary) AS totalSalary
FROM Salaries S
LEFT JOIN Master M
ON S.playerID = M.playerID
GROUP BY S.playerID
ORDER BY totalSalary DESC
LIMIT 1;

#d
SELECT AVG(sumHR) AS playerAvgHR
FROM ((SELECT playerID, sum(HR) AS sumHR FROM Batting
GROUP BY playerID) AS calcValues);

#e
#explain
Select sum(calcValues.sumHR)/COUNT(calcValues.pID) as playerAvgHR
FROM ((SELECT playerID AS pID, sum(HR) AS sumHR from Batting
where HR>0
group by playerID) as calcValues);

#f
#Average value of home runs per batter
#explain
Select sum(calcValues.sumHR)/COUNT(calcValues.pID) as playerAvgHR
FROM ((SELECT playerID AS pID, sum(HR) AS sumHR from Batting
group by playerID) as calcValues);

#e
explain
SELECT COUNT(B.playerID) AS goodPlayers FROM
(SELECT playerID, SUM(HR) AS totHR FROM Batting
GROUP BY playerID
HAVING totHR > (SELECT SUM(sumHR)/COUNT(pID) AS playerAvgHR
FROM (SELECT playerID AS pID, SUM(HR) AS sumHR FROM Batting
GROUP BY playerID) AS avgHR)) AS B
JOIN
(SELECT playerID, SUM(SHO) AS totSHO FROM Pitching
GROUP BY playerID
HAVING totsHO> (Select sum(sumSHO)/COUNT(pitchID) as avgSHO
FROM (SELECT playerID AS pitchID, sum(SHO) AS sumSHO FROM Pitching
GROUP BY playerID) AS avgSHO)) AS P
ON B.playerID = P.playerID;