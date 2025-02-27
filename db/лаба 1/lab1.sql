CREATE TABLE IF NOT EXISTS natural_scene (
    natural_scene_id SERIAL NOT NULL PRIMARY KEY,
    planet_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (planet_id) REFERENCES planet(planet_id)
);

CREATE TABLE IF NOT EXISTS planet (
    planet_id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS phenomena (
    phenomen_id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(12) NOT NULL,
    description VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS consequences (
    consequence_id SERIAL NOT NULL PRIMARY KEY,
    consequence VARCHAR(22) NOT NULL
);

CREATE TABLE IF NOT EXISTS phenomena_consequences (
    phenomen_id INT NOT NULL,
    consequence_id INT NOT NULL,
    PRIMARY KEY (phenomen_id, consequence_id),
    FOREIGN KEY (phenomen_id) REFERENCES phenomena(phenomen_id),
    FOREIGN KEY (consequence_id) REFERENCES consequences(consequence_id)
);

CREATE TABLE IF NOT EXISTS phenomena_in_scene (
    natural_scene_id INT NOT NULL,
    phenomen_id INT NOT NULL,
    PRIMARY KEY (natural_scene_id, phenomen_id),
    FOREIGN KEY (natural_scene_id) REFERENCES natural_scene(natural_scene_id),
    FOREIGN KEY (phenomen_id) REFERENCES phenomena(phenomen_id)
);

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
