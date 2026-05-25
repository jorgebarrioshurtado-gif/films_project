-- looking for the films with more budget

SELECT tf.*, tb.title 
FROM tmdb_financial tf
LEFT JOIN links l
ON tf.tmdb_id = l.tmdb_id
LEFT JOIN title_basics tb
ON l.imdb_id = tb.imdb_id
WHERE budget > 300000000;

-- looking which films there are in genome_scores

SELECT DISTINCT(gs.movie_id), tb.title
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id; 

-- how many films are there in genome scores and bechdel

SELECT DISTINCT(gs.movie_id), tb.title
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
INNER JOIN bechdel b
ON b.imdb_id = l.imdb_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id;

SELECT COUNT(DISTINCT(gs.movie_id))
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
INNER JOIN bechdel b
ON b.imdb_id = l.imdb_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id;


SELECT COUNT(DISTINCT(gs.movie_id))
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
INNER JOIN bechdel b
ON b.imdb_id = l.imdb_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id
WHERE b.rating = 3; 