DROP TABLE IF EXISTS bin;
DROP TABLE IF EXISTS fill_level;

--implicit rowid
CREATE TABLE bin (
  bin_name TEXT PRIMARY KEY,
  is_spill INTEGER CHECK(is_spill = 0 OR is_spill = 1),
  is_spill_updated TIMESTAMP DEFAULT (datetime('now','localtime')),
  is_tilt INTEGER CHECK(is_tilt = 0 OR is_tilt = 1),
  is_tilt_updated TIMESTAMP DEFAULT (datetime('now','localtime'))
);

--implicit rowid
CREATE TABLE fill_level (
  fill_percent INTEGER NOT NULL CHECK(fill_percent >= 0 AND fill_percent <= 100),
  time_updated TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL,
  bin_name TEXT NOT NULL, 
  FOREIGN KEY(bin_name) REFERENCES bin(bin_name)
);

CREATE TRIGGER is_spill_last_updated 
AFTER UPDATE OF is_spill ON bin
BEGIN
UPDATE bin SET is_spill_updated = (datetime('now','localtime')) WHERE bin_name = old.bin_name;
END;

CREATE TRIGGER is_tilt_last_updated 
AFTER UPDATE OF is_tilt ON bin
BEGIN
UPDATE bin SET is_tilt_updated = (datetime('now','localtime')) WHERE bin_name = old.bin_name;
END;

-- old trigger not needed
-- CREATE TRIGGER bin_last_updated BEFORE UPDATE ON bin
-- BEGIN
-- UPDATE bin SET last_updated = (datetime('now','localtime')) WHERE name = old.name;
-- END;

-- Initialise mock data
INSERT INTO bin (bin_name, is_spill, is_tilt) 
VALUES
  ('ALPHA', false, false)
;

INSERT INTO fill_level (bin_name, fill_percent, time_updated) 
VALUES
  ('ALPHA', 5, datetime('now', '-3 hours', 'localtime')),
  ('ALPHA', 10, datetime('now', '-2 hours', 'localtime')),
  ('ALPHA', 15, datetime('now', '-1 hours', 'localtime'))
;