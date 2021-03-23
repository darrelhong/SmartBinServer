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

CREATE TRIGGER is_spill_last_updated AFTER UPDATE ON bin
WHEN new.is_spill IS NOT NULL
BEGIN
UPDATE bin SET is_spill_updated = (datetime('now','localtime')) WHERE bin_name = old.bin_name;
END;

CREATE TRIGGER is_tilt_last_updated AFTER UPDATE ON bin
WHEN new.is_tilt IS NOT NULL
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
  ('alpha', false, false), 
  ('bravo', false, false),
  ('charlie', false, false),
  ('delta', false, false),
  ('echo', false, false)
;

INSERT INTO fill_level (bin_name, fill_percent, time_updated) 
VALUES
  ('alpha', 5, datetime('now', '-3 hours', 'localtime')),
  ('alpha', 10, datetime('now', '-2 hours', 'localtime')),
  ('alpha', 15, datetime('now', '-1 hours', 'localtime')),
  ('bravo', 20, datetime('now', '-30 minutes', 'localtime')),
  ('bravo', 25, datetime('now', '-25 minutes', 'localtime')),
  ('bravo', 30, datetime('now', '-20 minutes', 'localtime')),
  ('charlie', 35, datetime('now', '-45 minutes', 'localtime')),
  ('charlie', 40, datetime('now', '-40 minutes', 'localtime')),
  ('charlie', 45, datetime('now', '-35 minutes', 'localtime')),
  ('delta', 50, datetime('now', '-15 minutes', 'localtime')),
  ('delta', 55, datetime('now', '-10 minutes', 'localtime')),
  ('delta', 60, datetime('now', '-5 minutes', 'localtime')),
  ('echo', 75, datetime('now', '-30 seconds', 'localtime')),
  ('echo', 80, datetime('now', '-20 seconds', 'localtime')),
  ('echo', 85, datetime('now', '-10 seconds', 'localtime'))
;