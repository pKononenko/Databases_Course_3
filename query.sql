
-- FIRST QUERY

SELECT game_name, SUM(REGION_SALES) AS TOTAL_SALES
FROM GAMESALES
GROUP BY game_name
ORDER BY TOTAL_SALES;


-- SECOND QUERY

SELECT
    GameGenre.genre,
    round( count(*) * 100 / ( SELECT count(*) FROM gamegenre ), 2 ) as PERCENTAGE
FROM
    GameGenre
GROUP BY genre
ORDER BY PERCENTAGE DESC;


-- THIRD QUERY

SElECT 
    year_of_release,
    count(game_name)/4 AS GAMES_COUNT
FROM GAMESALES
GROUP BY year_of_release
ORDER BY year_of_release;
