-- looking the recommendations

SELECT DISTINCT(gs.movie_id), tb.title
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id
WHERE gs.movie_id = 219003;  -- 128099, 129514

SELECT DISTINCT(gs.movie_id), tb.title, tb.year
FROM genome_scores gs
LEFT JOIN links l
ON l.movie_id = gs.movie_id
LEFT JOIN title_basics tb
ON tb.imdb_id = l.imdb_id
WHERE tb.title = "George Carlin: It's Bad for Ya!"; 