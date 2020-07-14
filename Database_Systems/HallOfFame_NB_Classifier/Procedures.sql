-- Natalia Hoyos
-- Juan Manuel Gomez

# SET @db = 'lahman2016';
# USE lahman2016;

# select concat('DROP PROCEDURE IF EXISTS ', routine_name, ';') 
# from information_schema.routines 
# where routine_schema = 'lahman2016' 
# and routine_type = 'PROCEDURE';

DROP PROCEDURE IF EXISTS GetDBName;
DELIMITER $$
CREATE PROCEDURE GetDBName(IN db VARCHAR(32))    
BEGIN 
set @db = db;
END $$
DELIMITER ;

## Stored procedure to return column names and display them to the user for selection
DROP PROCEDURE IF EXISTS ColumnIdentifier;
DELIMITER $$
CREATE PROCEDURE ColumnIdentifier(tableName VARCHAR(32))    
BEGIN 
SET @tabName = tableName;
IF tableName = 'Managers' THEN
	SET SQL_SAFE_UPDATES=0;
		UPDATE Managers SET plyrMgr = 0 WHERE plyrMgr = 'N';
        UPDATE Managers SET plyrMgr = 1 WHERE plyrMgr = 'Y';   
    SET SQL_SAFE_UPDATES=1;

END IF;

SELECT COLUMN_NAME as column_name 
    FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME in ('HallOfFame', tableName) 
        AND TABLE_SCHEMA = @db
        AND COLUMN_NAME not in ('playerID', 'inducted', 'lgID', 'yearID', 'stint', 'teamID', 'votedby', 'category', 'needed_note', 'votes', 'ballots', 'needed', 'birthMonth', 'birthDay', 'deathMonth', 'deathDay')
        ORDER BY COLUMN_NAME;
END$$
DELIMITER ;

# CALL columnIdentifier('Batting');

## Master Stored Procedure
DROP PROCEDURE IF EXISTS MasterProcedure;
DELIMITER $$
CREATE PROCEDURE MasterProcedure(features VARCHAR(255), trainSize float)    
BEGIN
DECLARE Message VARCHAR(255);
CALL TableCreation(features);
CALL SplitData(trainSize);
CALL iterCategorical('Train');
CALL MapCategorical('Train', 'TrainCategorical');
CALL MapCategorical('Test', 'TestCategorical');
CALL ProbTable('TrainCategorical');
CALL IterNB();
#Getting the Accuracy
SELECT ROUND(1-sum(abs(candidate-predicted))/count(*), 3) into @mes FROM TestCategorical;
SET message = CONCAT('Accuracy: ', @mes);
#Getting the precision
SELECT ROUND(a.truePositive/b.pred, 3) into @mes1 from (select sum(predicted) as truePositive from TestCategorical WHERE predicted = candidate) as a, (SELECT SUM(predicted) as pred FROM TestCategorical) as b;
SET message = CONCAT(message, '\n Precision: ', @mes1);
SELECT ROUND(a.truePositive/b.cand, 3) into @mes2 from (select sum(predicted) as truePositive from TestCategorical WHERE predicted = candidate) as a, (SELECT SUM(candidate) as cand FROM TestCategorical) as b;
SET message = CONCAT(message, '\n Recall: ', @mes2);
Select message;
END$$
DELIMITER ;

# SET @tabname = 'Batting';
# CALL MasterProcedure('`2B` `3B` AB BB CS G GIDP H HBP HR IBB R RBI SB SF SH SO',  0.8);
# # CALL MasterProcedure('`2B` `3B` `AB` `BB` `CS` `G` `GIDP` `H` `HBP` `HR` `IBB` `R` `RBI` `SB` `SF` `SH` `SO`', 0.7);

# SET @tabname = 'Managers';
# 	SET SQL_SAFE_UPDATES=0;
# 		UPDATE Managers SET plyrMgr = 0 WHERE plyrMgr = 'N';
#         UPDATE Managers SET plyrMgr = 1 WHERE plyrMgr = 'Y';   
#     SET SQL_SAFE_UPDATES=1;
# CALL MasterProcedure('G L W inseason plyrMgr `rank`', 0.7);
# # SELECT @mes;

# SELECT * FROM Managers;

# Select count(`rank`) from managers;
# Select count(`rank`) from managers where `rank` is not null; 

# SELECT 1-sum(abs(candidate-predicted))/count(*) FROM TestCategorical;
# SELECT count(candidate) from TestCategorical;
# SELECT count(predicted) from TestCategorical;

## Stored Procedure to Create Mining Table
DROP PROCEDURE IF EXISTS TableCreation;
DELIMITER $$
CREATE PROCEDURE TableCreation(features VARCHAR(255))    
BEGIN 
## Initializing variables
DECLARE i int;
SET @feat = features;

 ## Clean Table
 DROP TABLE IF EXISTS `Mining`;
 
 ## Get requested table and features selected 
 # Prepare Query
 SET @mining = CONCAT('CREATE TABLE Mining as select playerID,');
 
 SET i = 1;
 WHILE ISNULL(NULLIF(@feat, '')) = 0 DO
	SET @mining = CONCAT_WS(' ', @mining, 'AVG(', (SELECT SUBSTRING_INDEX(@feat, ' ', 1)), ') as', (SELECT SUBSTRING_INDEX(@feat, ' ', 1)),',');
	SET @feat = (SELECT TRIM(leading SUBSTRING_INDEX(@feat, ' ', 1) from @feat));	
	SET @feat = (SELECT TRIM(leading from @feat));
    SET i = i + 1;
END WHILE;

SET @mining = CONCAT_WS(' ', @mining, '(MAX(inducted) IS NOT NULL) AS candidate FROM', @tabName, 'LEFT JOIN HallOfFame USING(playerID) group by playerID'); 

#Execute Query 
PREPARE query0 FROM @mining;  
EXECUTE query0; 
DEALLOCATE PREPARE query0;     
END$$ 
DELIMITER ;

# SET @tabName = 'Batting';
# CALL tableCreation('G CS SF GIDP');
# CALL tableCreation('G AB R H `2B` `3B` HR RBI SB CS BB SO IBB HBP SH SF GIDP');

## Stored Procedure to Split the Data
DROP PROCEDURE IF EXISTS SplitData;
DELIMITER $$ 
CREATE PROCEDURE SplitData(trainSize float) 
BEGIN 
  ## Initializing variables
  -- DECLARE Total, Tot0, Tot1, train0, train1, test0, test1 float DEFAULT 0; 
  
  ## Getting Totals
  SET @Total = (SELECT COUNT(DISTINCT playerID )
 FROM Mining); 
  SET @Tot0 = (SELECT COUNT(DISTINCT playerID )
	FROM Mining where candidate=0); 
  SET @Tot1 = (SELECT COUNT(DISTINCT playerID ) 
	FROM Mining where candidate=1); 
    
  ## Calculating Rates 
  SET @train1 =  ROUND(((@Tot1 / @Total) * trainSize) * @Total); 
  
  SET @test1  =  ROUND(((@Tot1 / @Total) * (1-trainSize)) * @Total); 
  
  ## Removing Existing Tables
  DROP TABLE IF EXISTS Train; 
  DROP TABLE IF EXISTS Test; 
  DROP TABLE IF EXISTS Class0; 
  DROP TABLE IF EXISTS Class1; 

  ## Creating Base Tables
  CREATE TABLE  Class0 as
	SELECT * FROM Mining where candidate=0; 
  CREATE TABLE Class1  as
	SELECT * FROM Mining where candidate=1; 
    
  ## Creating Training and Test Tables
  SET @get_test0 = CONCAT('CREATE TABLE Test AS SELECT * FROM Class0 ORDER BY RAND() LIMIT ', @test1); 
  PREPARE query0 FROM @get_test0; 
  EXECUTE query0; 

  SET @get_train0 = CONCAT('CREATE TABLE Train AS SELECT * FROM Class0 WHERE playerID NOT IN (SELECT playerID FROM Test) LIMIT ', @train1);
  PREPARE query1 FROM @get_train0; 
  EXECUTE query1; 
      
  SET @get_test1 = CONCAT('INSERT INTO Test SELECT * FROM Class1 ORDER BY RAND() LIMIT ', @test1); 
  PREPARE query2 FROM @get_test1; 
  EXECUTE query2; 
      
  SET @get_train1 = CONCAT('INSERT INTO Train SELECT * FROM Class1 WHERE playerID NOT IN (SELECT playerID FROM Test) LIMIT ', @train1); 
  PREPARE query3 FROM @get_train1; 
  EXECUTE query3; 

  ## Dropping Unused Tables 
  DROP TABLE IF EXISTS Class0; 
  DROP TABLE IF EXISTS Class1; 
  
  DEALLOCATE PREPARE query0; 
  DEALLOCATE PREPARE query1; 
  DEALLOCATE PREPARE query2; 
  DEALLOCATE PREPARE query3; 

END$$ 
DELIMITER ;

# CALL SplitData(0.7);

### Based on  https://jonlabelle.com/snippets/view/sql/mysql-median-implementation (median)  and  https://stackoverflow.com/a/4951354 (loop over columns)
DROP PROCEDURE IF EXISTS Insert_Medians;
DELIMITER $$
Create PROCEDURE Insert_Medians(IN fea_name varchar(20),IN med_val double)
    BEGIN
    insert into Medians(`feature`, `median`) values (fea_name, med_val);
    END ;
$$
DELIMITER ;

## Getting the medians to split the continuous values
DROP PROCEDURE IF EXISTS Median;
DELIMITER $$
CREATE PROCEDURE Median(tbl VARCHAR(32), col VARCHAR(32))
BEGIN
  DECLARE arg VARCHAR(64);
  SET @sql0 = CONCAT( 'SELECT ((COUNT(*))/2) INTO @c FROM ', tbl );
  PREPARE stmt FROM @sql0;
  EXECUTE stmt;
  DROP PREPARE stmt;
  SET @a = CONVERT(FLOOR(@c), SIGNED);
  IF @a = @c THEN
    BEGIN
      SET @a = @a-1;
      SET @b = 2;
      SET arg = CONCAT( 'AVG(`', col, '`)' );
    END;
  ELSE
    BEGIN
      SET @b = 1;
      SET arg = CONCAT('`', col, '`');
    END;
  END IF;
  SET @sql1 = CONCAT('SELECT ', arg, ' INTO @res FROM (SELECT `', col, '` FROM ', tbl,
                    ' ORDER BY `', col, '` LIMIT ?,?) as tmp');
  PREPARE stmt FROM @sql1;
  EXECUTE stmt USING @a, @b;
  DROP PREPARE stmt;
  CALL insert_medians(col, @res);
END;
$$
DELIMITER ;

# CALL Median('Batting','G');

DROP PROCEDURE IF EXISTS IterCategorical;
DELIMITER $$
CREATE PROCEDURE IterCategorical(tble VARCHAR(32))
BEGIN
    -- DECLARE num_rows2 int;
    DECLARE done INT DEFAULT 0;
    DECLARE i int;
    DECLARE col_name varCHAR(32);
    DECLARE col varCHAR(32);
    DECLARE num_col int;

	DECLARE col_names CURSOR FOR
		SELECT column_name
		FROM INFORMATION_SCHEMA.COLUMNS
		WHERE table_name in (tble)
		AND TABLE_SCHEMA = @db
		ORDER BY ordinal_position;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    DROP TABLE IF EXISTS Medians;
    CREATE TABLE Medians (feature VARCHAR(20) NOT NULL DEFAULT '', median double);

	SET i = 1;
    OPEN col_names;
	SELECT FOUND_ROWS() into num_col;
    
	FETCH col_names 
	INTO col_name;
	the_loop: LOOP
		SET i = i + 1; 
	   IF i > num_col-1 THEN
			CLOSE col_names;
			LEAVE the_loop;
		END IF;

		FETCH col_names 
		INTO col_name;
        SET col = col_name;

         CALL Median(tble, col);
		 
	END LOOP the_loop;
END $$
DELIMITER ;

# CALL iterCategorical('Train');

## Procedure to map features into categories
DROP PROCEDURE IF EXISTS Threshold;
DELIMITER $$
CREATE PROCEDURE Threshold(tbl VARCHAR(32), col VARCHAR(32))
BEGIN  
	IF col != 'candiate' THEN
		SET SQL_SAFE_UPDATES=0;

		SET @sql0 = CONCAT(' ','SELECT median INTO @medi from Medians where feature = "', col, '"');
		PREPARE stmt FROM @sql0;
		EXECUTE stmt;
		DROP PREPARE stmt;
		
		SET @sql1 = CONCAT('UPDATE ', tbl, ' SET `', col, '` = 0 WHERE `', col, '` <= ', @medi);
		PREPARE stmt FROM @sql1;
		EXECUTE stmt;
		DROP PREPARE stmt;
		
		SET @sql1 = CONCAT('UPDATE ', tbl, ' SET `', col, '` = 1 WHERE `', col, '` > ', @medi);
		PREPARE stmt FROM @sql1;
		EXECUTE stmt;
		DROP PREPARE stmt;
		
		SET SQL_SAFE_UPDATES=1;
    END IF;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS MapCategorical;
DELIMITER $$
CREATE PROCEDURE MapCategorical(tbl1 VARCHAR(32), tbl2 VARCHAR(32))
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE i int;
    DECLARE col_name varCHAR(32);
    DECLARE col varCHAR(32);
    DECLARE num_col int;

	DECLARE col_names CURSOR FOR
		SELECT column_name
		FROM INFORMATION_SCHEMA.COLUMNS
		WHERE table_name in (tbl1)
		AND TABLE_SCHEMA = @db
		ORDER BY ordinal_position;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;	
    
	SET @sql0 = CONCAT('DROP TABLE IF EXISTS ', tbl2);
    PREPARE stmt FROM @sql0;
    EXECUTE stmt;
    DROP PREPARE stmt;
    
    SET @sql1 = CONCAT('CREATE TABLE ', tbl2,  ' AS SELECT * FROM ', tbl1);
    PREPARE stmt FROM @sql1;
    EXECUTE stmt;
    DROP PREPARE stmt;  

	SET i = 1;
    OPEN col_names;
	SELECT FOUND_ROWS() into num_col;

	FETCH col_names 
	INTO col_name;
	other_loop: LOOP
		SET i = i + 1; 
	   IF i > num_col-1 THEN
			CLOSE col_names;
			LEAVE other_loop;
		END IF;

		FETCH col_names 
		INTO col_name;
        SET col = col_name;
        IF col != 'playrMgr' THEN
			CALL Threshold(tbl2, col);
        END IF;
	END LOOP other_loop;
END $$
DELIMITER ;

# CALL MapCategorical('Train', 'TrainCategorical');
# CALL MapCategorical('Test', 'TestCategorical');

## stored procedure to compute probabilities
DROP PROCEDURE IF EXISTS Insert_Prob;
DELIMITER $$
Create PROCEDURE Insert_Prob(tbl varchar(32),col varchar(32))
    BEGIN
    SET @probfc1 = 0.0;
    SET @probfc0 = 0.0;
    
    -- SELECT ROUND((sum(col)/count(col))/100, 3) into @probf from train;
	SET @sql0 = CONCAT('SELECT 1-(sum(`', col, '`)/count(`', col, '`)) into @probf0 from ', tbl);
	PREPARE stmt FROM @sql0;
	EXECUTE stmt;
	DROP PREPARE stmt;
    
    --  SELECT (sum(col)/count(col))/100 into @probfc1 from train WHERE candidate = 0;
	SET @sql1 = CONCAT('SELECT 1-(sum(`', col, '`)/count(`', col, '`)) into @probf0c1 from ', tbl, ' WHERE candidate = 0');
	PREPARE stmt FROM @sql1;
	EXECUTE stmt;
	DROP PREPARE stmt;
    
--    --  SELECT (sum(col)/count(col))/100 into @probfc0 from train WHERE candidate = 1;
-- 	SET @sql2 = CONCAT('SELECT 1-ROUND(sum(', col, ')/count(', col, '), 3) into @probf0c0 from ', tbl, ' WHERE candidate = 1');
-- 	PREPARE stmt FROM @sql2;
-- 	EXECUTE stmt;
-- 	DROP PREPARE stmt;
    
    INSERT INTO Prob(feature, probfea, probFeatureClass0) values (col, @probf0, @probf0c1);
    END ;
$$
DELIMITER ;

DROP PROCEDURE IF EXISTS ProbTable;
DELIMITER $$
Create PROCEDURE ProbTable(tbl1 varchar(64))
    BEGIN
	DECLARE done INT DEFAULT 0;
    DECLARE i int;
    DECLARE num_col int;
    DECLARE col_name varCHAR(32);
    DECLARE col varCHAR(32);

	DECLARE col_names CURSOR FOR
		SELECT column_name
		FROM INFORMATION_SCHEMA.COLUMNS
		WHERE table_name in (tbl1)
		AND TABLE_SCHEMA = @db
		ORDER BY ordinal_position;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
	DROP TABLE IF EXISTS Prob;
    CREATE TABLE Prob(feature VARCHAR(16), probfea double, probFeatureClass0 double);
    
	SET i = 1;
    OPEN col_names;
    SELECT FOUND_ROWS() into num_col;

	FETCH col_names 
	INTO col_name;
	Another_loop: LOOP
		SET i = i + 1; 
	   IF i > num_col-1 THEN
			CLOSE col_names;
			LEAVE Another_loop;
		END IF;

		FETCH col_names 
		INTO col_name;
        SET col = col_name;
        Call insert_prob(tbl1, col);
	END LOOP Another_loop;
   
    END $$
DELIMITER ;

# CALL ProbTable('TrainCategorical');

DROP PROCEDURE IF EXISTS PredictNB;
DELIMITER $$
Create PROCEDURE PredictNB(tbl VARCHAR(32), col VARCHAR(32), last_ int)
BEGIN
	SET SQL_SAFE_UPDATES=0;
	SELECT probFeatureClass0 into @probfc from Prob where feature = col;
    
	SET @sql1 = CONCAT(' UPDATE ', tbl, ' SET Probability = Probability * abs(`', col, '`-(@probfc))');
	PREPARE stmt FROM @sql1;
	EXECUTE stmt;
	DROP PREPARE stmt;

	SELECT probfea into @probfea from Prob where feature = col;
	SET @sql2 = CONCAT(' UPDATE ', tbl, ' SET Probability = Probability / (abs(`', col, '`-(@probfea)))');
	PREPARE stmt FROM @sql2;
	EXECUTE stmt;
	DROP PREPARE stmt;

    IF last_ = 1 THEN
		SELECT sum(candidate)/count(candidate) into @probc from TrainCategorical;
		
        SET @sql3 = CONCAT(' UPDATE ', tbl, ' SET Probability = Probability * (1-@probc)');
		PREPARE stmt FROM @sql3;
		EXECUTE stmt;
		DROP PREPARE stmt;
        
        SET @sql4 = CONCAT(' UPDATE ', tbl, ' SET Predicted = 1 WHERE Probability < 0.5');
		PREPARE stmt FROM @sql4;
		EXECUTE stmt;
		DROP PREPARE stmt;
       
    END IF;
    SET SQL_SAFE_UPDATES=1;    
END$$
DELIMITER ;

# SET SQL_SAFE_UPDATES=0;
# ALTER TABLE TestCategorical ADD COLUMN probability VARCHAR(15) AFTER candidate;
# ALTER TABLE TestCategorical ADD COLUMN predicted VARCHAR(15) AFTER probability;
# UPDATE TestCategorical SET probability = 1, predicted = 0;
# SET SQL_SAFE_UPDATES=1;

# CALL predictNB('TestCategorical', 'G', 1);


DROP PROCEDURE IF EXISTS IterNB;
DELIMITER $$
Create PROCEDURE IterNB()
BEGIN 
    DECLARE done INT DEFAULT 0;
    DECLARE i int;
    DECLARE col_name varCHAR(32);
    DECLARE col varCHAR(32);
    DECLARE num_col int;
    DECLARE last_ int;

	DECLARE col_names CURSOR FOR
		SELECT column_name
		FROM INFORMATION_SCHEMA.COLUMNS
		WHERE table_name in ('TestCategorical')
		AND TABLE_SCHEMA = @db
		ORDER BY ordinal_position;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    # Last column flag
	SET last_=0;
    
    SET SQL_SAFE_UPDATES=0;
    
    IF EXISTS ( SELECT * FROM information_schema.columns WHERE table_name = 'TestCategorical' AND column_name = 'probability' AND table_schema = @db) THEN
		ALTER TABLE TestCategorical DROP COLUMN probability;
	END IF;
    
	IF EXISTS ( SELECT * FROM information_schema.columns WHERE table_name = 'TestCategorical' AND column_name = 'predicted' AND table_schema = @db) THEN
		ALTER TABLE TestCategorical DROP COLUMN predicted;
	END IF;
    
    ALTER TABLE TestCategorical
	ADD COLUMN probability VARCHAR(15) AFTER candidate;
    
	ALTER TABLE TestCategorical
	ADD COLUMN predicted VARCHAR(15) AFTER probability;
   
	UPDATE TestCategorical SET probability = 1, predicted = 0;
	SET SQL_SAFE_UPDATES=1;

	SET i = 1;
    OPEN col_names;    
	SELECT FOUND_ROWS() into num_col;
        
	FETCH col_names 
	INTO col_name;
	yet_another_loop: LOOP
		SET i = i + 1; 
	   IF i > num_col-1 THEN
			CLOSE col_names;
			LEAVE yet_another_loop;
		END IF;

		FETCH col_names 
		INTO col_name;
        SET col = col_name;
        
		IF i = num_col-1 THEN
			Set last_ = 1;
		END IF;

         Call PredictNB('TestCategorical', col, last_);
		 
	END LOOP yet_another_loop;
END$$
DELIMITER ;

# Call IterNB();

DROP PROCEDURE IF EXISTS GetTest;
DELIMITER $$
CREATE PROCEDURE GetTest()    
BEGIN 
SELECT playerID FROM Test ORDER BY playerID;
END $$
DELIMITER ;

# CALL GetTest();

DROP PROCEDURE IF EXISTS GetTestData;
DELIMITER $$
CREATE PROCEDURE GetTestData(player VARCHAR(32))    
BEGIN 
	DROP TABLE IF EXISTS Temp;
    CREATE TABLE Temp SELECT * FROM Test WHERE playerID = player;
    
	IF EXISTS ( SELECT * FROM information_schema.columns WHERE table_name = 'Temp' AND column_name = 'candidate' AND table_schema = @db) THEN
		ALTER TABLE Temp DROP COLUMN candidate;
	END IF;
    
    SELECT * FROM Temp WHERE playerID = player LIMIT 1;
    
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS GetClass;
DELIMITER $$
CREATE PROCEDURE GetClass(player VARCHAR(32), Class VARCHAR(32) )    
BEGIN 
    SET @sql0 = CONCAT('SELECT ', Class, ' FROM TestCategorical WHERE playerID = "', player, '" LIMIT 1;');
	PREPARE stmt FROM @sql0;
	EXECUTE stmt;
	DROP PREPARE stmt;    
END $$
DELIMITER ;

# CALL GetClass('JuanMa', predicted);
# CALL GetClass('JuanMa', candidate);
# SELECT * FROM testCategorical;

# # CALL GetTestData('hibbsji01');

# SELECT * FROM testcategorical;
# SET @tabname = 'Batting';
# CALL MasterProcedure('`2B` `3B` `AB` `BB` `CS` `G` `GIDP` `H` `HBP` `HR` `IBB` `R` `RBI` `SB` `SF` `SH` `SO`', 0.7);
