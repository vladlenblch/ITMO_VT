DROP TABLE IF EXISTS phenomena_in_scene;
DROP TABLE IF EXISTS phenomena_consequences;
DROP TABLE IF EXISTS natural_scene;
DROP TABLE IF EXISTS phenomena;
DROP TABLE IF EXISTS consequences;
DROP TABLE IF EXISTS planet;

CREATE TABLE IF NOT EXISTS planet (
    planet_id SERIAL PRIMARY KEY,
    name VARCHAR(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS natural_scene (
    natural_scene_id SERIAL PRIMARY KEY,
    planet_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (planet_id) REFERENCES planet(planet_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS phenomena (
    phenomen_id SERIAL PRIMARY KEY,
    name VARCHAR(12) NOT NULL,
    description VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS consequences (
    consequence_id SERIAL PRIMARY KEY,
    consequence VARCHAR(22) NOT NULL
);

CREATE TABLE IF NOT EXISTS phenomena_consequences (
    phenomen_id INT NOT NULL,
    consequence_id INT NOT NULL,
    PRIMARY KEY (phenomen_id, consequence_id),
    FOREIGN KEY (phenomen_id) REFERENCES phenomena(phenomen_id) ON DELETE CASCADE,
    FOREIGN KEY (consequence_id) REFERENCES consequences(consequence_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS phenomena_in_scene (
    natural_scene_id INT NOT NULL,
    phenomen_id INT NOT NULL,
    FOREIGN KEY (natural_scene_id) REFERENCES natural_scene(natural_scene_id) ON DELETE CASCADE,
    FOREIGN KEY (phenomen_id) REFERENCES phenomena(phenomen_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION check_phenomenon_uniqueness()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM phenomena_in_scene 
        WHERE natural_scene_id = NEW.natural_scene_id 
        AND phenomen_id = NEW.phenomen_id
    ) THEN
        RAISE EXCEPTION 'Природное явление (ID: %) уже присутствует в сцене (ID: %)', 
        NEW.phenomen_id, NEW.natural_scene_id;
    ELSE
        PERFORM 1 FROM phenomena_in_scene;
    END IF;
    
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_phenomenon_uniqueness
BEFORE INSERT OR UPDATE ON phenomena_in_scene
FOR EACH ROW
EXECUTE FUNCTION check_phenomenon_uniqueness();

INSERT INTO planet (name) VALUES
('Юпитер');

INSERT INTO phenomena (name, description) VALUES
('вихри', NULL), 
('порывы ветра', 'ураганные'),
('потоки газа', 'восходящие'),
('воронка', 'гигантская');

INSERT INTO consequences (consequence) VALUES
('нарушать строй облаков'),
('раскрывать пелену'),
('открывать вид'),
('низвергаться в глубины');

INSERT INTO natural_scene (planet_id, timestamp) VALUES
(1, '2025-03-03 12:00:00'),
(1, '2025-03-03 14:00:00');

INSERT INTO phenomena_consequences (phenomen_id, consequence_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO phenomena_in_scene (natural_scene_id, phenomen_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4);

SELECT * from natural_scene;
SELECT * from planet;
SELECT * from phenomena_in_scene;
SELECT * from phenomena;
SELECT * from phenomena_consequences;
SELECT * from consequences;
