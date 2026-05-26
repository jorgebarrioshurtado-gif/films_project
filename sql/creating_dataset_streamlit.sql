-- creating the table for streamlit app

SELECT DISTINCT l.tmdb_id, tb.*, tr.avg_rating, b.rating, c.cluster
FROM links l 
RIGHT JOIN genome_scores gs
ON gs.movie_id = l.movie_id
LEFT JOIN title_basics tb
ON l.imdb_id = tb.imdb_id
LEFT JOIN title_ratings tr
ON l.imdb_id = tr.imdb_id
LEFT JOIN bechdel b
ON l.imdb_id = b.imdb_id
LEFT JOIN clusters c
ON c.movie_id = l.movie_id;