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
  ('alpha', true, false), 
  ('bravo', false, true),
  ('charlie', false, false),
  ('delta', false, false),
  ('echo', false, false)
;

INSERT INTO fill_level (bin_name, fill_percent, time_updated) 
VALUES
  ('alpha', 5, datetime('now', '-12 minutes', 'localtime')),
  ('alpha', 6, datetime('now', '-11 minutes', 'localtime')),
  ('alpha', 15, datetime('now', '-10 minutes', 'localtime')),
  ('alpha', 20, datetime('now', '-9 minutes', 'localtime')),
  ('alpha', 22, datetime('now', '-8 minutes', 'localtime')),
  ('alpha', 25, datetime('now', '-7 minutes', 'localtime')),
  ('alpha', 26, datetime('now', '-6 minutes', 'localtime')),
  ('alpha', 27, datetime('now', '-5 minutes', 'localtime')),
  ('alpha', 34, datetime('now', '-4 minutes', 'localtime')),
  ('alpha', 5, datetime('now', '-3 minutes', 'localtime')),
  ('alpha', 8, datetime('now', '-2 minutes', 'localtime')),
  ('alpha', 14, datetime('now', '-1 minutes', 'localtime')),

  ('bravo', 67, datetime('now', '-12 minutes', 'localtime')),
  ('bravo', 78, datetime('now', '-11 minutes', 'localtime')),
  ('bravo', 83, datetime('now', '-10 minutes', 'localtime')),
  ('bravo', 88, datetime('now', '-9 minutes', 'localtime')),
  ('bravo', 96, datetime('now', '-8 minutes', 'localtime')),
  ('bravo', 0, datetime('now', '-7 minutes', 'localtime')),
  ('bravo', 4, datetime('now', '-6 minutes', 'localtime')),
  ('bravo', 34, datetime('now', '-5 minutes', 'localtime')),
  ('bravo', 46, datetime('now', '-4 minutes', 'localtime')),
  ('bravo', 51, datetime('now', '-3 minutes', 'localtime')),
  ('bravo', 62, datetime('now', '-2 minutes', 'localtime')),
  ('bravo', 71, datetime('now', '-1 minutes', 'localtime')),

  ('charlie', 32, datetime('now', '-12 minutes', 'localtime')),
  ('charlie', 34, datetime('now', '-11 minutes', 'localtime')),
  ('charlie', 46, datetime('now', '-10 minutes', 'localtime')),
  ('charlie', 56, datetime('now', '-9 minutes', 'localtime')),
  ('charlie', 60, datetime('now', '-8 minutes', 'localtime')),
  ('charlie', 61, datetime('now', '-7 minutes', 'localtime')),
  ('charlie', 63, datetime('now', '-6 minutes', 'localtime')),
  ('charlie', 77, datetime('now', '-5 minutes', 'localtime')),
  ('charlie', 5, datetime('now', '-4 minutes', 'localtime')),
  ('charlie', 26, datetime('now', '-3 minutes', 'localtime')),
  ('charlie', 30, datetime('now', '-2 minutes', 'localtime')),
  ('charlie', 31, datetime('now', '-1 minutes', 'localtime')),

  ('delta', 7, datetime('now', '-12 minutes', 'localtime')),
  ('delta', 12, datetime('now', '-11 minutes', 'localtime')),
  ('delta', 22, datetime('now', '-10 minutes', 'localtime')),
  ('delta', 43, datetime('now', '-9 minutes', 'localtime')),
  ('delta', 45, datetime('now', '-8 minutes', 'localtime')),
  ('delta', 54, datetime('now', '-7 minutes', 'localtime')),
  ('delta', 63, datetime('now', '-6 minutes', 'localtime')),
  ('delta', 79, datetime('now', '-5 minutes', 'localtime')),
  ('delta', 12, datetime('now', '-4 minutes', 'localtime')),
  ('delta', 19, datetime('now', '-3 minutes', 'localtime')),
  ('delta', 27, datetime('now', '-2 minutes', 'localtime')),
  ('delta', 39, datetime('now', '-1 minutes', 'localtime')),

  ('echo', 22, datetime('now', '-12 minutes', 'localtime')),
  ('echo', 24, datetime('now', '-11 minutes', 'localtime')),
  ('echo', 36, datetime('now', '-10 minutes', 'localtime')),
  ('echo', 56, datetime('now', '-9 minutes', 'localtime')),
  ('echo', 82, datetime('now', '-8 minutes', 'localtime')),
  ('echo', 99, datetime('now', '-7 minutes', 'localtime')),
  ('echo', 9, datetime('now', '-6 minutes', 'localtime')),
  ('echo', 12, datetime('now', '-5 minutes', 'localtime')),
  ('echo', 23, datetime('now', '-4 minutes', 'localtime')),
  ('echo', 43, datetime('now', '-3 minutes', 'localtime')),
  ('echo', 50, datetime('now', '-2 minutes', 'localtime')),
  ('echo', 62, datetime('now', '-1 minutes', 'localtime'))
;