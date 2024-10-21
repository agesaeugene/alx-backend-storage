-- Task 12: Average weighted score - generates a stored procedure. 
-- Compute Average Weighted Score For User calculates and saves the 
-- average weighted score for a student. user_id, a users.id value 
-- (you can presume user_id is associated with an existing user)
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    DECLARE w_avg_score FLOAT;
    SET w_avg_score = (SELECT SUM(score * weight) / SUM(weight)
                        FROM users AS U
                        JOIN corrections as C ON U.id=C.user_id
                        JOIN projects AS P ON C.project_id=P.id
                        WHERE U.id=user_id);
    UPDATE users SET average_score = w_avg_score WHERE id=user_id;
END
|
DELIMITER ;



