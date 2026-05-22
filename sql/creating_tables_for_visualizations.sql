-- quick overview of all the datasets

SELECT *
FROM bechdel;

SELECT *
FROM genome_scores;

SELECT *
FROM genome_tags;

SELECT *
FROM links;

SELECT *
FROM ratings;

SELECT *
FROM title_basics;

SELECT *
FROM title_ratings;

SELECT *
FROM tmdb_financial;


-- creating the big dataset for tableau

SELECT l.imdb_id, 
		tb.title, tb.year, tb.runtime_min,
        tf.budget, tf.revenue,
        tr.avg_rating, tr.num_votes,
        b.rating, b.dubious 
FROM links l
LEFT JOIN title_basics tb
ON l.imdb_id = tb.imdb_id
LEFT JOIN bechdel b
ON tb.imdb_id = b.imdb_id
LEFT JOIN title_ratings tr
ON l.imdb_id = tr.imdb_id
LEFT JOIN tmdb_financial tf
ON l.tmdb_id = tf.tmdb_id;

-- in order not to mess the main dataset and keep it clean we'll create two other datasets,
-- one for ratings of movielens users and another for the films genres
-- they will be handy for some visualizations and will be joined through the imdb_id 
 
SELECT l.imdb_id, r.user_id, r.rating
FROM links l
LEFT OUTER JOIN ratings r
ON l.movie_id = r.movie_id;


SELECT l.imdb_id, tg.genre
FROM links l
LEFT OUTER JOIN title_genres tg
ON l.imdb_id = tg.imdb_id;














