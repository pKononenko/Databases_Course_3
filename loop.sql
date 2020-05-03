
-- Заповнення за допомогою LOOP таблиці GAMEGENRE

DECLARE
   
    -- Кількість рядків
    num_rows INT NOT NULL DEFAULT 4;
    
    TYPE arr_names IS VARRAY(5) OF GAME.game_name%TYPE;
    TYPE arr_genres IS VARRAY(5) OF GENRE.genre%TYPE;
    
    -- Масив назв ігор та жанрів
    game_names arr_names;
    genre_names arr_genres;

BEGIN

    genre_names := arr_genres('Shooter', 'Shooter', 'Action', 'Arcade');
    game_names := arr_names('Call of Duty', 'Medal of Honor', 'Grand Theft Auto III', 'Super Mario Bros.');
    
    -- Заповнимо батьківські таблиці перед дочірніми
    -- Game
    FOR idx in 1..num_rows LOOP
    
        INSERT INTO GAME
        VALUES (game_names(idx));
    
    END LOOP;
    
    -- Genre (заповнюємо insert для уникнення дублікатів)
    INSERT INTO GENRE
    VALUES ('Shooter');
    
    INSERT INTO GENRE
    VALUES ('Arcade');
    
    INSERT INTO GENRE
    VALUES ('Action');
    
    -- Заповнюємо дочірню таблицю GAMEGEMRE за допомогою LOOP, яка відповідає вимогам
    -- (в таблиці є два атрибути)
    
    FOR idx in 1..num_rows LOOP
    
        INSERT INTO GAMEGENRE
        VALUES (game_names(idx), genre_names(idx));
    
    END LOOP;
    
END;
