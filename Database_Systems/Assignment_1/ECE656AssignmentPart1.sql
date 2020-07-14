/*
ECE 656
Assignment 1, Part 1
Juan Manuel Gomez Gonzalez
*/

#(a) By unknown birthdates it will be assumed that the day, and/or month and/or year of its birthdate is not known:
SELECT COUNT(bDay.playerID) AS missingBDay
FROM(
	SELECT playerID, birthYear, birthMonth, birthDay
	FROM Master
	WHERE birthYear=0
	OR birthMonth=0
	OR birthday=0) AS bDay;
#There are 449 players with a missing day, month or year (or a combination of those fields).

/*
(b) It can be assumed that people present in the table HallOfFame that do not have a corresponding deathYear (empty field) 
in Master are alive, and therefore the people with an assigned deathYear are dead. The table HallOfFame includes repeated 
information (same players in different years or in the same year but through another type of nomination) and should only be 
counted once. This can be achieved by grouping the players according to their ID ("GROUP BY playerID") and its resulting 
deathYear can be obtained by using the AVG function, which in turn would return a 0 for the rows that have an empty deathYear
or the average deathYear between the same player, which in kind returns the same deathYear. Afterwards, a conditional can be 
used to check if the deathYear is bigger than 0 or if it is equal to 0, and depending of this conditional it can be counted 
as a 1 or a -1, as shown:
*/
SELECT SUM(IF(deadOrAlive.avgDeath> 0, -1, 1)) AS aliveMinusDeadPlayers
FROM(
	SELECT HOF.playerID, avg(M.deathYear) as avgDeath
	FROM HallOfFame HOF
	LEFT JOIN Master M
	ON HOF.playerID = M.playerID
	GROUP BY HOF.playerID) as deadOrAlive;
/*
The result of this query is -46, which means there are 46 more dead players than alive players.
When the subquery SELECT HOF.playerID... is run without the aggregating function and the GROUP BY statement, it is seen that 
there is a player, whose playerID is drewj.01,  is present in the HallOfFame table but not in the Master table. This player 
is therefore missing its deathYear (its represented as NULL) and when the average function is run would be counted as having
an average deathYear of 0. Although it is important to be observant of a NULL value and what it could carry in the end result,
as it is only one missing row in a dead or alive subtraction it means that the ending result would be changed by either a
positive one or a negative one (positive in our case).  The value is still in the negative range and still means that there
are more dead than alive players.

(c)The tables Master and Salaries must be related (joined) in order to calculate the total salaries of the players. There 
will also be repeated instances of the same player winning playing multiple years and in different teams, so the players 
must be grouped into one instance each, to be able of finding the total salary. The LIMIT element forces MySQL to only show 
the first line of the result for the query.
*/
SELECT S.playerID, nameFirst, nameLast, SUM(salary) AS totalSalary
FROM Salaries S
LEFT JOIN Master M
ON S.playerID = M.playerID
GROUP BY S.playerID
ORDER BY totalSalary DESC
LIMIT 1;
/*
The player with the highest total salary is Alex Rodriguez with a total salary of $398,416,252. Some players do not have 
a corresponding playerID in the Master table, so it would not be possible to know their real names but instead it would 
be necessary to reference them by their playerID if they were the players with the highest salaries. 

### (d)
The average home runs per player can be calculated by finding the total value of home runs found in the batting table 
divided by counting all the (distinct) players present in the same table.
*/
SELECT AVG(sumHR) AS playerAvgHR
FROM ((SELECT playerID, sum(HR) AS sumHR FROM Batting
GROUP BY playerID) AS calcValues);
/*
This returns an average home run value of 15.29 between 18915 players. The problem with this approach is that it assumes 
that the Batting table has all the players that have played baseball, which might not be true for some pitchers or fielders 
if they have not batted (and thus are not in the table). Another approach would be to count all the homeruns present in the 
Teams table and divide it by the total number of players in the Master table, without counting the managers who were not players. 
This can be achieved with:
*/
SELECT ((SELECT SUM(HR) FROM Teams)/(SELECT COUNT(Players.playerID) 
FROM
	(SELECT Mas.playerID 
	FROM Master AS Mas
	LEFT OUTER JOIN (SELECT playerID, plyrMgr from Managers WHERE plyrMgr LIKE 'N') AS Man
	ON Mas.playerID = Man.playerID
	WHERE Man.playerID IS NULL) AS Players)) AS avgHR;
/*
This in turn gives us an average home run per player value of 15.58 between 18573 players. The difference between both averages 
found is about 0.3, or almost 2%. This could be attributed to the player discrepancy found (a difference of about 400 players 
between both queries), but at the same time could be considered that the averages of both approaches are almost equal taking 
into account that there are more than 18,000 players in the database, which at the same time has statistical values taken as 
far back as the second half of the 1800's (and might not be as accurate).

(e) In order to find the average home runs per player, with the condition of only counting players that have had at least one
home run, the WHERE clause can be used in order to filter out the players with a HR score of 0. Using the first approach mentioned
in question d it can be found that:
*/
Select sum(calcValues.sumHR)/COUNT(calcValues.pID) as playerAvgHR
FROM ((SELECT playerID AS pID, sum(HR) AS sumHR from Batting
where HR>0
group by playerID) as calcValues);
/*
This returns an average of 37.39. The same cannot be done using the second approach used in the previous question, as that query 
uses the total value of Home Runs per team per year, not the home runs per player and therefore it cannot be found what players to 
exclude from the count.

(f) Using the query obtained in question (d), it is possible to obtain again the average home run per batter:
*/

#Average value of home runs per batter
Select sum(calcValues.sumHR)/COUNT(calcValues.pID) as playerAvgHR
FROM ((SELECT playerID AS pID, sum(HR) AS sumHR from Batting
group by playerID) as calcValues);

/*
Giving a value of 15.29. A similar query would give the average ShutOut value for the Pitchers:
*/

#Average value of ShutOuts per pitcher
Select sum(pitValues.sumSHO)/COUNT(pitValues.pitchID) as avgSHO
FROM ((SELECT playerID AS pitchID, sum(SHO) AS sumSHO from Pitching
group by playerID) as pitValues);

/*
Giving a value of approximately 2.17. Both of these queries can then be combined used as the limit values to filter the players who
have a better than average home runs and shutout scores:
*/

# Comparison Query
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

/*
39 players have more than the average number of Home Runs and more than the average number of ShutOut Games and therefore can be
considered to be both good batters and good pitchers according to the definition in question f.

#--------------------------------------------------------------------------------------------------------------------------------------

## 2.
The LOAD statement must include the LOCAL parameter as it is being loaded from a local computer to the server. The CSV has each
field separated by a comma, and each row of data separated by a new line and a carriage return (CR). This should be included as
well so that the file loads the values correctly (some columns become seemingly distorted after using the SELECT * query if the
CR is not included). The first row contains a row of headers, which can be ignored during the loading of the file with the 
IGNORE X LINES parameter. Some of the values in the fields that have a type INT are missing, and would cause an error loading the
file if the sql_mode is set to a restrictive value. This can be avoided by specifying that the "blank" values of the file be replaced
with a value or NULL using the SET clause. The REPLACE parameter would make the new input rows replace the existing ones, but this
only happens if the Table has a Primary Key already associated to it. In the case of the Fielding Table it will generate a new row
of almost identical data instead of replacing it as the table is missing a Primary Key. In question 3 it is found that the lack of
a primary key would create a problem as it would not be possible to create the key of the table with this conflicting data (all the
fields that would need to be unique would not be after loading this file), so it is necessary to run the primary key creation before
loading the new data:
*/

#Primary key creation
ALTER TABLE Fielding
ADD PRIMARY KEY (playerID, yearID, stint, POS);

#Data loading
LOAD DATA LOCAL INFILE '~/Desktop/Fielding.csv' REPLACE INTO TABLE Fielding
  FIELDS TERMINATED BY ',' lines terminated by '\r\n' IGNORE 1 LINES
(playerID, yearID,stint,teamID,lgID,POS,@vG,GS,InnOuts,@vPO,@vA,@vE,@vDP,PB,WP,SB,CS,ZR)
SET
G = nullif(@vG,''),
PO = nullif(@vPO,''),
A = nullif(@vA,''),
E = nullif(@vE,''),
DP = nullif(@vDP,'');

#--------------------------------------------------------------------------------------------------------------------------------------

/*
3.
The correct way of incorporating the Primary Keys (PK) and Foreign Keys (FK) is to create them before inputting the data, this way it
reduces the possible spread of errors or "bad" information. The PK was obtained by checking which field or combination of fields did not
have duplicate values and that were not unique data to a specific field, e.g. playerID or yearID. When a key failed to be created because
it was not unique, that row in aprticular was looked at to see what other fields could be included into the PK creation, that made that
particular row unique. 

It is more reasonable to create the tables with their respective keys and before introducing dta, in order to make sure that all of
the information is correctly added to the database. In this case the information is already in the tables and most likely will cause
problems when adding the foreign keys to the respective tables, as it is possible to encounter for example playerIDs that are not present
in the Master table (that should theoretically contain all the players of the database) but are present in other tables. This can be
solved by adding the missing data to their respective tables and cleaning up duplicates/erroneous data, etc. This approach,
although feasible, would be out of the scope of the assignment as it would involve getting in touch with the manager of the
database in order to make sure all the fields that would be changed are being correctly changed, the general distribution of
the tables’ PK and FK are being selected correctly, etc. For this specific case the command "foreign_key_checks = 0" can be used,
and will allow the creation of the FK, but to avoid any more inconveniences it is better to just use it in the tables that are
having conflicting data.

For the PK creation, this was done as follows:

#### Master table
As mentioned in the readme for the database, the playerID field in the Master table gives a unique code for each player, and can be
used as the Primary Key (PK) for that table.
*/
ALTER TABLE Master
ADD PRIMARY KEY (playerID);
/*
#### Batting and Pitching tables
The Batting, Pitching, and Fielding do not benefit of the uniqueness of playerID, as a player can play multiple years in the same 
teams or in different teams. Looking at the data in the tables it seems that the playerID, yearID and stint could be used as a PK
for these tables. 
This tables can then be assigned a unique key with the constraints set to its playerID, yearID, and stint.
*/

ALTER TABLE Batting
ADD CONSTRAINT battingID PRIMARY KEY (playerID, yearID, stint);
ALTER TABLE Pitching
ADD CONSTRAINT pitchingID PRIMARY KEY (playerID, yearID, stint);
/*
#### Fielding table
The problem with the Fielding table is that there are repeated values for some players as they might have played in the same game
and year but on different positions (e.g. "addybo01" played in 1871 in second base and in shortstop during the same game). This
means that for the Fielding table another field must be selected to guarantee uniqueness in the PK's values. This seems to be
achievable using the POS field of the Fielding Tables in addition to the previously selected playerID, yearID and stint values.
This would be enough for the original Fielding table, but the table being currently used has duplicate values that resulted from
the LOAD statement used on Question 2 of Part 1. A solution to this problem is removing the duplicate values, another would be
assigning the PK before loading the .CSV file (this time the REPLACE method would help in avoiding the duplicates), a third method
would be to create a new field which would work as an index, have unique values and be assigned as the PK of the table. In this
homework the second method was selected and therefore the Fielding table already has the PK. The PK will still be shown here but
in a commented format:
*/

#Line was already run in question 2 so will be commented here:
/*
ALTER TABLE Fielding
ADD CONSTRAINT fieldingID PRIMARY KEY (playerID, yearID, stint, POS);
*/

/* 
#### AllstarFull table
For the AllstarFull table, the fields of playerID and yearID is assumed that can be used as a primary key, as it might be possible
for a player to be in that game in various years, but would not play in different teams or leagues in the same year. This returned
an error as there where duplicate values for the PK, and after looking at the table to confirm this, it can be seen that for example
aparilu01 did indeed play two AllStar games in 1959. It was found afterwards that there were a couple of years after World War II in
which the All Star Games were played two times per year instead of the (assumed) one time per year. This means that the gameNum field
must also be included in the PK constraint.
*/
ALTER TABLE AllstarFull
ADD CONSTRAINT allSstarfullID PRIMARY KEY (playerID, yearID, gameNum);
/*
####HallOfFame table
For the HallOfFame table, the playerID, yearID and votedBy can be used as it can be assumed that a player cannot be nominated to
the Hall of Fame more than one time per year per each voting method.
*/
ALTER TABLE HallOfFame
ADD CONSTRAINT halloffameID PRIMARY KEY (playerID, yearID, votedBy);

/*
#### Managers table
For the Managers table it is reasonable to assume that the primary key be defined by the playerID and yearID. After looking at
the table it can be seen that inseason should also be included in the PK, as for example in 1968 lopezal01 was the third and fifth
manager in the CHA team and thus would be considered a duplicate using the PK without an inseason.
*/
ALTER TABLE Managers
ADD CONSTRAINT managersID PRIMARY KEY (playerID, yearID, inseason);

/*
#### Teams table
For the Teams table the values of yearID, lgId, and teamID should be used.
*/
ALTER TABLE Teams
ADD CONSTRAINT teamsID PRIMARY KEY (yearID, lgId, teamID);

/*
#### BattingPost and PitchingPost tables
For the tables of BattingPost and PitchingPost it can also be seen that the playerID and yearID will not be enough for the PK,
similar to the case of the Batting and Pitching tables. Therefore, the fields of playerID, yearID and round can be used for the
PK of these tables like shown:
*/
ALTER TABLE BattingPost
ADD CONSTRAINT battingpostID PRIMARY KEY (yearID, round, playerID);

ALTER TABLE PitchingPost
ADD CONSTRAINT pitchingpostID PRIMARY KEY (yearID, round, playerID);

/*
#### TeamsFranchises table
The TeamsFranchises table can have a PK based on its franchID field:
*/
ALTER TABLE TeamsFranchises
ADD CONSTRAINT teamsfranchisesID PRIMARY KEY (franchID);

/*
#### FieldingOF table
The FieldingOF table has similar data to the other Fielding tables, and as it has repetitive values for the same playerID in
different years (and even in the same year but with a different stint) the need for a third variable, stint, is needed.
*/

ALTER TABLE FieldingOF
ADD CONSTRAINT fieldingof PRIMARY KEY (playerID, yearID, stint);

/*
#### ManagersHalf table
As a manager might manage more than one time in their lifetime, and might manage more than one team in the same year, the
playerID, yearID, teamID and inseason should be used for the PK. Using those fields as a PK generates an error due to there
being managers who were present during both halves of a season, so the half field must also be included.
*/

ALTER TABLE ManagersHalf
ADD CONSTRAINT managershalfID PRIMARY KEY (playerID, yearID, teamID, inseason, half);

/*
#### TeamsHalf table
For the TeamsHalf table the yeatID, teamID and Half seem enough to become a PK:
*/
ALTER TABLE TeamsHalf
ADD CONSTRAINT teamshalfID PRIMARY KEY (yearID, teamID, half);

/*
#### Salaries table
It is logical to assume that a player might have played baseball for more than one year, and that depending of what 
team they were playing his salary would change. 
*/
ALTER TABLE Salaries
ADD CONSTRAINT salariesID PRIMARY KEY (yearID, teamID, playerID);

/*
#### SeriesPost table
Looking at the data in SeriesPost, it can be seen that the table has repetitive values for the year, but in combination
with the round it might be enough to be a Primary Key.
*/
ALTER TABLE SeriesPost
ADD CONSTRAINT seriespostID PRIMARY KEY (yearID, round);

/*
#### AwardsManagers table
The data in the AwardsManagers table indicated that the playerID, yearID and awardID can be a PK.
*/
ALTER TABLE AwardsManagers
ADD CONSTRAINT awardsmanagersID PRIMARY KEY (playerID, awardID, yearID);

/*
#### AwardsPlayers table
Similar to the AwardsManagers table, this table's PK can be created using the playerID, yearID and awardID. On running that
command, it is found that in fact the player with a playerID of bresnro01in 1908 won the same award two times, one for each league.
This means that the PK must also contain the lgID field.
*/
ALTER TABLE AwardsPlayers
ADD CONSTRAINT awardsplayersID PRIMARY KEY (playerID, awardID, yearID, lgID);

/*
#### AwardsShareManagers table
A PK for the AwardsShareManagers table seems to be obtainable using the awardID, yearID, and playerID:
*/

ALTER TABLE AwardsShareManagers
ADD CONSTRAINT awardssharemanagersID PRIMARY KEY (awardID, yearID, playerID);

/*
#### AwardsSharePlayers table
The same fields used for AwardsSahreManagers can be used for the AwardsSharePlayers, as it is:
*/
ALTER TABLE AwardsSharePlayers
ADD CONSTRAINT awardsshareplayersID PRIMARY KEY (awardID, yearID, playerID);

/*
#### FieldingPost table
As in the Fielding table, the playerID, yearID and round in the FieldingPost are not enough to become the PK, and it will be
necessary to add the POS field:
*/
ALTER TABLE FieldingPost
ADD CONSTRAINT fieldingpostID PRIMARY KEY (playerID, yearID, round, POS);

/*
#### Appearances table
The appearances table's PK seems to be able of being created with the yearID, teamID and playerID:
*/
ALTER TABLE Appearances
ADD CONSTRAINT appearancesID PRIMARY KEY (yearID, teamID, playerID);

/*
#### Schools
The schools table has a list of the baseball schools used to learn Baseball, and as so it is seemingly impossible to have two
schools with the same ID, and as such the schoolID can be used as the table's primary key:
*/
ALTER TABLE Schools
ADD CONSTRAINT schoolsID PRIMARY KEY (schoolID);

/*
#### CollegePlaying
As a player might play in different colleges and in different years throughout his study time, the only possible PK for
this table is a combination of all of the three fields in the table:
*/
ALTER TABLE CollegePlaying
ADD CONSTRAINT collegeplayingID PRIMARY KEY (playerID, schoolID, yearID);

/*
#### FieldingOFsplit
This table has the same structure as the other Fielding related tables, and therefore the PK will also be similar:
*/
ALTER TABLE FieldingOFsplit
ADD CONSTRAINT fieldingofsplitID PRIMARY KEY (playerID, yearID, stint);

/*
#### Parks
The parks table seems to be uniquely identified using the park.key field (which must be mentioned in the query using
a backtick to avoid problems in MySQL):
*/
ALTER TABLE Parks
ADD PRIMARY KEY (`park.key`);

#### HomeGames
ALTER TABLE HomeGames
ADD CONSTRAINT homegamesID PRIMARY KEY (`year.key`,`team.key`,`park.key`);


### Foreign keys

ALTER TABLE Batting
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Batting
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE Pitching
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Pitching
ADD FOREIGN KEY (yearID,teamID,lgID) REFERENCES Teams(yearID,teamID,lgID);

ALTER TABLE Fielding
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Fielding
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE AllStarFull
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE AllStarFull
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE Managers
ADD FOREIGN KEY (playerID) REFERENCES Master (playerID);
ALTER TABLE Managers
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE Teams
ADD FOREIGN KEY (franchID) REFERENCES TeamsFranchises(franchID);

ALTER TABLE BattingPost
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Batting
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE PitchingPost
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Pitching
ADD FOREIGN KEY (yearID,teamID,lgID) REFERENCES Teams(yearID,teamID,lgID);

#TeamsFranchises has no foreign keys

ALTER TABLE FieldingOF
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE ManagersHalf
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE ManagersHalf
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);
ALTER TABLE ManagersHalf
ADD FOREIGN KEY (playerID, yearID, inseason) REFERENCES Managers(playerID, yearID, inseason);

ALTER TABLE TeamsHalf
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE SeriesPost
ADD FOREIGN KEY (yearID, lgIDwinner, teamIDwinner) REFERENCES Teams(yearID, lgID, teamID);
ALTER TABLE SeriesPost
ADD FOREIGN KEY (yearID, lgIDloser, teamIDloser) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE AwardsManager
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE AwardsPlayers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE AwardsShareManagers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE AwardsSharePlayers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE FieldingPost
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE FieldingPost
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE Appearances
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Appearances
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE CollegePlaying
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

#Schools doesn't have FK

ALTER TABLE FieldingOFsplit
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE FieldingOFsplit
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

#Parks doesn't have FK

ALTER TABLE HomeGames
ADD Foreign KEY (`park.key`) REFERENCES Parks(`park.key`);
ALTER TABLE HomeGames
ADD FOREIGN KEY (`year.key`, `league.key`, `team.key`) REFERENCES Teams(yearID, lgID, teamID);

#The FK for the HallOfFame, Salaries and CollegePlaying that are the ones having conflicting data:
SET foreign_key_checks = 0;

ALTER TABLE HallOfFame
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

ALTER TABLE Salaries
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);
ALTER TABLE Salaries
ADD FOREIGN KEY (yearID, lgID, teamID) REFERENCES Teams(yearID, lgID, teamID);

ALTER TABLE CollegePlaying
ADD FOREIGN KEY (schoolID) REFERENCES School(schoolID);

#Turn back on foreign key check
SET foreign_key_checks = 1;