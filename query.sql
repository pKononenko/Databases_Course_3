
-- FIRST QUERY

SELECT 
    game_name,
    SUM(REGION_SALES) AS TOTAL_SALES
FROM GAMESALES
GROUP BY game_name
ORDER BY TOTAL_SALES DESC;


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



-- VIEW QUERIES
-- FIRST QUERY

SELECT 
    game_name, 
    SUM(REGION_SALES) AS TOTAL_SALES
FROM GAMEDATA
GROUP BY game_name
ORDER BY TOTAL_SALES DESC;


-- SECOND QUERY

SELECT
    genre,
    round( count(DISTINCT game_name) * 100 / ( SELECT count(*) FROM (SELECT DISTINCT GAME_NAME FROM GAMEDATA) ) , 2) AS PERCENTAGE
FROM GAMEDATA
GROUP BY genre
ORDER BY PERCENTAGE DESC;


-- THIRD QUERY

SElECT 
    year_of_release,
    count(game_name)/4 AS GAMES_COUNT
FROM GAMEDATA
GROUP BY year_of_release
ORDER BY year_of_release;
