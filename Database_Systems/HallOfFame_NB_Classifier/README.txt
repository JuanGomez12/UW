ECE656 Winter 2019 Project

Natalia Hoyos Velasquez and Juan Manuel Gomez Gonzalez.


This project looks to predict the probability of a player from the Lahman database to be nominated to the Hall of Fame, using a Naive Bayes classifier implemented in SQL using a GUI designed in Python. This particular exercise disregards if the player is inducted or not and focuses on predicting if the player was nominated. The Python portion is only for visualizing the data, the predictions are calculated using SQL directly.

Setup:
-- MYSQL
1- In MySQL, run the DBCreation.sql file in order to create a new Lahman Baseball database with the name ProjectNB.

2- Run the Procedures.sql file in order to create the required stored procedures for the Database.

-- The required python packages can be found in the requirements.txt file located within this project's folder.
To automatically install these dependencies the following command can be used:
   pip install -r requirements.txt


Instructions to use:

Run ECE656_Project.py

1. Press "Enter" to access the program.

2. Enter the database information (host, user, password and database name) so that it can access the baseball database. A copy of it can be accessed in the accompanying .sql file, which when run using the workbench will create a copy of the database calling it ECE656_Project. After entering all the required information, press "Open DB".

3. Select the table to use for the classification, either "Batting", "Pitching" or "Managers".

4. A list of possible features to use for the classification will be displayed in the listbox. Select any number of features that you want to use.

5. Select the percentage that will be used for the train - test split. This percentage of the samples will be used to train the classifier, with the remaining used to test it.

6. Press the "Create Classifier" button and wait for the server to return a result. The textbox after the button will show the classifier performance scores obtained by using the selected features.

7. Using the following listbox, select a player for which you want to predict if they are going to be nominated to the Hall of Fame.

8. Press the "Predict Class" button to predict if the selected player will be nominated to the Hall Of Fame. This will also show the real outcome (Class) of the sample.


More info:

This project intends to reduce the amount of network traffic. All the data storage, manipulation and splitting, and the classifier training, testing and evaluation is performed using stored procedures on the database. A full database table is never transmitted. Python is only used as a tool to build the GUI.

In total, the Client makes 7 calls to the Server and the server responds with the following:
- doesn't return anything one time
- returns one row or one column three times
- returns a string three times.

## Data Preprocessing:

Sanity checks where performed in the database, and errors in the database where encountered:
Players that won the hall of fame award did not have their respective batting/pitching/manager statistics for that particular year, e.g. the player aaronha01 was inducted into the Hall Of Fame (HOF) in 1982 but does not have any statistics for that particular year. Another example can be seen with the player abbotji01, which was nominated in 2005 but there are no Batting/Pitching/Managers statistics for this particular player.
	If the correct combination of playerID and yearID was performed, e.g. a join between the Batting and the HOF table was performed using both playerID and yearID, it was only possible to obtain statistics for one player inducted into the Hall of Fame and 26 that were nominated but were not inducted. Due to this, it was decided to better use the average of the statistics of each player and compare it with the induction into the HOF. With this, two classes were created: the players who were nominated to the HOF (both inducted and just nominated, so those who are present on the HOF table) and those not nominated to the HOF (and thus not present in the HOF table).

Categorization:
Most features on the database are numeric and they had to be transformed into categories.
It was decided for practical uses to divide each feature into two categories based on the median. The average was not chosen because most of the features were found to be highly skewed. This way every player would have a feature either above the median or under the median.



## Stored Procedures:

ColumnIdentifier: It receives the name of the table chosen by the user in the Client and based on that returns a list of features for the user to pick for the creation of the classifier.

TableCreation: It receives the names of the features that will be used for the classification and generates a table with only the features selected by the client and a column indicating if the player is present on the HallOfFame table.

SplitData: It receives the train size percentage selected by the client and randomly splits the table into test and train tables preserving the positive and negative proportions.

IterCategorical: Receives the table name (Train). It identifies the columns that the table has, creates an empty `Medians` table, and iterates over the detected columns. By calling the Median stored procedure it calculates the median of the feature. This value is then sent to a `Medians` table which is created populated by the InsertMedians stored procedure.

MapCategorical: It receives the name of the table (Test or Train) and the name of the table in which to store the mapping. It copies the original table into the new table and calls a stored procedure named Threshold. This Threshold procedure categorizes each player's statistics from the selected features into 1 if they are greater than the median or 0 if they are equal to or lesser than the median.

ProbTable: Receives the name of the table (Train) and creates the probability table based on that table's selected features. The `Prob` table contains the different probabilities needed to compute the naive Bayes classifier. To populate this table, the procedure iterates over the selected features while calling a secondary stored procedure (i.e. Insert_Prob), which in turn calculates the previously mentioned probabilities.

IterNB: Computes the resulting probability of each sample from the Test set to be a candidate for the HallOfFame. It does so by iterating over the column and with the help of the PredictNB stored procedure it multiplies and divides by the corresponding probability. It also selects and stores the predicted class.

MasterProcedure: Receives the features chosen by the client, the total number of features that were chosen and the train-test split percentage selected by the user. Controls and runs the former mentioned procedures except ColumnIdentifier.

GetTest: Returns the playerID of all the samples from the testing set. This way the Client can display it for the user to choose which sample to inspect closer.

GetTestData: Returns the feature values stored for the specific playerID selected by the user.

GetClass: Receives the playerID and if it wants the real class or the predicted class. Returns the corresponding class for the specific playerID selected by the user.
