/*
ECE 656
Assignment 1, Part 2
Juan Manuel Gomez Gonzalez
*/

/*
(a)
This query can be obtained by counting the number of reviews each member has in the review table or by looking at the
review_count column of the user table:

#First method:
SELECT user_id as UID, COUNT(review_id) AS countRev FROM review r
GROUP BY user_id
ORDER BY countRev DESC
LIMIT 1;

This returns a review count of 1,427 on a user_id of kGgAARL2UmvCcTRfiscjug. When the name for this value is looked for 
in the user table, it seems to not exist as the review and user tables only have 100 values in common.
*/
#Second method:
SELECT user_id, name, review_count FROM user
ORDER BY review_count DESC
LIMIT 1;
/*
With this second method you obtain a review count of 11,284 reviews with the name Victor and user_id of 8k3aO-mPeyhbR5HUucA5aA.
Again, when looked upon in the review table, this user seems to be missing.

(b)
*/
SELECT business_id, name, review_count FROM business
GROUP BY business_id, name
ORDER BY review_count DESC
LIMIT 1;
/*
The result of using this query is that the Mon Ami Gabi, with business_id of 4JNXUYY8wbaaDmk3BPzlWw, has the biggest amount
of reviews with a number of 6,414.


SELECT business_id, count(review_id) as revCount from review
GROUP BY business_id
ORDER BY revCount DESC
LIMIT 1;


This query results in a review count of 4,137 and the business_id of 4bEjOyTaDG24SY5TxsaUNQ, which also does not appear in 
the business table (similar to question a). Similarly, the business_id of Mon Ami Gabi does not appear in the review table.
*/

/*
(c)
This result can be obtained also using two methods, with the average value of the review_count value found in the user table
or with the division between the count of all the reviews and the count of (unique, or grouped) users in the review table.


#Method 1
SELECT AVG(review_count) AS avgReviews FROM user;


This query returns a result of 24.32 reviews per user.
*/

#Method 2
SELECT (SUM(Rev.count)/count(Rev.UID)) AS avgReviews FROM (SELECT user_id as UID, COUNT(review_id) AS count FROM review
GROUP BY user_id) AS Rev;

/*
This query in turn returns a value of 4.28 reviews per user. This discrepancy between the methods can be attributed to
the difference in users found in both the user and review table (1,029,432 and 366815, respectively) and thus returns
such different values.

(d)
*/
SELECT COUNT(diffUser.avgDif) AS diffUsers FROM (SELECT (avgTable.userAvg - avgTable.revAvg) AS avgDif FROM (SELECT userRev.avgStars AS userAvg, reviews.avgStars AS revAvg FROM (SELECT user_id AS UID, average_stars AS avgStars FROM user) AS userRev
JOIN (SELECT user_id AS UID, avg(stars) AS avgStars FROM review
GROUP by user_id) AS reviews
ON userRev.UID = reviews.UID) AS avgTable
WHERE ABS(avgTable.userAvg - avgTable.revAvg)>0.5) AS diffUser;

/*
66 users have a difference of 0.5 or more between their average ratings in their user and their review tables.

(e)
There are two approaches to this question, the simple and the complex one. First the complex one:
As the user and review tables seem to have different rows, it is possible to calculate the number of users in the union of both
tables in order to obtain the totality of the users in the database:

# Users present in the review table
SELECT COUNT(review_id), user_id FROM review GROUP BY user_id;
366,815 rows

# Users present in the user table
SELECT u.user_id, u.review_count FROM user u
1,029,432

Put together, both queries should then be added 1,029,432+366,815 for a total amount of 1,396,147 when you subtract the 100 rows both
tables have in common.

Both tables can then be combined using a union:

#Total users in the database counting duplicates
SELECT rev.UID, rev.revCount FROM (SELECT COUNT(r.review_id) AS revCount, r.user_id AS UID FROM review r
GROUP BY user_id) AS rev
UNION
SELECT u.user_id, u.review_count FROM user u

Ends up returning 1,396,242 values, or 95 values more than what was expected. Using a query that removes the repeated user_id values:

SELECT rev.UID, rev.revCount FROM (SELECT COUNT(r.review_id) AS revCount, r.user_id AS UID FROM review r
GROUP BY user_id) AS rev
LEFT OUTER JOIN user u
ON rev.UID = u.user_id
WHERE u.user_id IS NULL;

And using is as part of the union query:

#Total users in the database
SELECT COUNT(totReviews.totcount) FROM (SELECT filteredReview.UID, filteredReview.revCount AS totCount FROM (select rev.UID as UID, rev.revCount AS revCount FROM (SELECT COUNT(r.review_id) AS revCount, r.user_id AS UID FROM review r
GROUP BY user_id) AS rev
LEFT OUTER JOIN user u
ON rev.UID = u.user_id
WHERE u.user_id is null) AS filteredReview
UNION
SELECT u.user_id, u.review_count FROM user u) AS totReviews;

Returns 1,396,147 rows, which is what was expected. It is now needed to filter the values with a review count lower than 10 and count the number of users with that minimum of reviews:

SELECT (SELECT COUNT(filteredRev.totalRevCount) AS totalReviewCount FROM (SELECT totalRev.revCount AS totalRevCount FROM (SELECT filteredReview.UID, filteredReview.revCount FROM (select rev.UID AS UID, rev.revCount AS revCount FROM (SELECT COUNT(r.review_id) AS revCount, r.user_id AS UID FROM review r
GROUP BY user_id) AS rev
LEFT OUTER JOIN user u
ON rev.UID = u.user_id
WHERE u.user_id IS NULL) AS filteredReview
UNION
SELECT u.user_id, u.review_count FROM user u) AS totalRev
WHERE revCount>10) AS filteredRev)
/(SELECT COUNT(totReviews.totcount) FROM (SELECT filteredReview.UID, filteredReview.revCount AS totCount FROM (select rev.UID as UID, rev.revCount AS revCount FROM (SELECT COUNT(r.review_id) AS revCount, r.user_id AS UID FROM review r
GROUP BY user_id) AS rev
LEFT OUTER JOIN user u
ON rev.UID = u.user_id
WHERE u.user_id is null) AS filteredReview
UNION
SELECT u.user_id, u.review_count FROM user u) AS totReviews) AS userFraction;

The result of that query is 365,928/1,396,147=0.26. This means that 26% of the users in the database have written more than 10 reviews.

Another approach, much more simple but not including all of the data present in the database is:
Calculate the amount of users that have more than 10 reviews in the user table, and divide it by the total of the users in the same table:

SELECT ((SELECT count(user_id) FROM user WHERE review_count>10)/(SELECT COUNT(user_id) from user)) AS userFraction;

This query returns 0.33, which means that 33% of the users present in the user table have written more than 10 reviews. The disadvantage
with this approach is that negates all the users that exist in the review table, thus meaning the totality of the users present in the
database are not being taken into account.

The problem with the last query is that it cannot be used in question (f), as it does not deal with 
*/
SELECT ((SELECT count(*)
FROM (SELECT count(review_id) AS countRev
FROM review GROUP BY user_id HAVING countRev>10) AS revCount)
/
(SELECT COUNT(*)
FROM (SELECT count(review_id)
FROM review GROUP BY user_id) AS totCount)) AS userFraction;
/*
This query returns 0.0685, which means that about 7% of the reviewers have more than 10 reviews.

(f)
The user table does not have the texts of the reviews, so the review table by itself will need to be used. The length() and char_length()
functions can be used to calculate the length of each review, but length() returns the length of the string in bytes while char_length()
returns the length in characters, which is more logical to use for this context.
*/

SELECT (sumTxt/sumRev)
FROM (SELECT sum(sumTxt) AS sumTxt, sum(countRev) AS sumRev
	FROM (SELECT sum(txtLength) AS sumTxt, count(review_id) AS countRev
		FROM (SELECT CHAR_LENGTH(text) AS txtLength, user_id AS UID, review_id FROM review) AS rev
		GROUP BY UID) AS sumRev
	WHERE countRev>10) AS totSumRev;
    
/*
The result of the query is that in average there are approximately 758 characters in each of the reviews posted by users present in the
reviews table and who have written more than 10 reviews.
*/