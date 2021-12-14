--list the names of all people who have directed a movie that received a rating of at least 9.0.

SELECT name FROM people
JOIN directors ON people.id = directors.person_id
JOIN movies ON movies.id = directors.movie_id
JOIN ratings ON ratings.movie_id = movies.id
WHERE ratings.rating >= 9;