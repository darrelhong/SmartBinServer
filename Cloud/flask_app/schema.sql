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
  ('ALPHA', true, false), 
  ('BRAVO', false, true),
  ('CHARLIE', false, false),
  ('DELTA', false, false),
  ('ECHO', false, false)
;

INSERT INTO fill_level (bin_name, fill_percent, time_updated) 
VALUES
  ('ALPHA', 5, datetime('now', '-12 minutes', 'localtime')),
  ('ALPHA', 6, datetime('now', '-11 minutes', 'localtime')),
  ('ALPHA', 15, datetime('now', '-10 minutes', 'localtime')),
  ('ALPHA', 20, datetime('now', '-9 minutes', 'localtime')),
  ('ALPHA', 22, datetime('now', '-8 minutes', 'localtime')),
  ('ALPHA', 25, datetime('now', '-7 minutes', 'localtime')),
  ('ALPHA', 26, datetime('now', '-6 minutes', 'localtime')),
  ('ALPHA', 27, datetime('now', '-5 minutes', 'localtime')),
  ('ALPHA', 34, datetime('now', '-4 minutes', 'localtime')),
  ('ALPHA', 5, datetime('now', '-3 minutes', 'localtime')),
  ('ALPHA', 8, datetime('now', '-2 minutes', 'localtime')),
  ('ALPHA', 14, datetime('now', '-1 minutes', 'localtime')),

  ('BRAVO', 67, datetime('now', '-12 hours', 'localtime')),
  ('BRAVO', 78, datetime('now', '-11 hours', 'localtime')),
  ('BRAVO', 83, datetime('now', '-10 hours', 'localtime')),
  ('BRAVO', 88, datetime('now', '-9 hours', 'localtime')),
  ('BRAVO', 96, datetime('now', '-8 hours', 'localtime')),
  ('BRAVO', 0, datetime('now', '-7 hours', 'localtime')),
  ('BRAVO', 4, datetime('now', '-6 hours', 'localtime')),
  ('BRAVO', 34, datetime('now', '-5 hours', 'localtime')),
  ('BRAVO', 46, datetime('now', '-4 hours', 'localtime')),
  ('BRAVO', 51, datetime('now', '-3 hours', 'localtime')),
  ('BRAVO', 62, datetime('now', '-2 hours', 'localtime')),
  ('BRAVO', 92, datetime('now', '-1 hours', 'localtime')),

  ('CHARLIE', 32, datetime('now', '-12 days', 'localtime')),
  ('CHARLIE', 34, datetime('now', '-11 days', 'localtime')),
  ('CHARLIE', 46, datetime('now', '-10 days', 'localtime')),
  ('CHARLIE', 56, datetime('now', '-9 days', 'localtime')),
  ('CHARLIE', 60, datetime('now', '-8 days', 'localtime')),
  ('CHARLIE', 61, datetime('now', '-7 days', 'localtime')),
  ('CHARLIE', 63, datetime('now', '-6 days', 'localtime')),
  ('CHARLIE', 77, datetime('now', '-5 days', 'localtime')),
  ('CHARLIE', 5, datetime('now', '-4 days', 'localtime')),
  ('CHARLIE', 26, datetime('now', '-3 days', 'localtime')),
  ('CHARLIE', 30, datetime('now', '-2 days', 'localtime')),
  ('CHARLIE', 31, datetime('now', '-1 days', 'localtime')),

  ('DELTA', 7, datetime('now', '-12 minutes', 'localtime')),
  ('DELTA', 12, datetime('now', '-11 minutes', 'localtime')),
  ('DELTA', 22, datetime('now', '-10 minutes', 'localtime')),
  ('DELTA', 43, datetime('now', '-9 minutes', 'localtime')),
  ('DELTA', 45, datetime('now', '-8 minutes', 'localtime')),
  ('DELTA', 54, datetime('now', '-7 minutes', 'localtime')),
  ('DELTA', 63, datetime('now', '-6 minutes', 'localtime')),
  ('DELTA', 79, datetime('now', '-5 minutes', 'localtime')),
  ('DELTA', 12, datetime('now', '-4 minutes', 'localtime')),
  ('DELTA', 19, datetime('now', '-3 minutes', 'localtime')),
  ('DELTA', 27, datetime('now', '-2 minutes', 'localtime')),
  ('DELTA', 76, datetime('now', '-1 minutes', 'localtime')),

  ('ECHO', 22, datetime('now', '-12 minutes', 'localtime')),
  ('ECHO', 24, datetime('now', '-11 minutes', 'localtime')),
  ('ECHO', 36, datetime('now', '-10 minutes', 'localtime')),
  ('ECHO', 56, datetime('now', '-9 minutes', 'localtime')),
  ('ECHO', 82, datetime('now', '-8 minutes', 'localtime')),
  ('ECHO', 99, datetime('now', '-7 minutes', 'localtime')),
  ('ECHO', 9, datetime('now', '-6 minutes', 'localtime')),
  ('ECHO', 12, datetime('now', '-5 minutes', 'localtime')),
  ('ECHO', 23, datetime('now', '-4 minutes', 'localtime')),
  ('ECHO', 43, datetime('now', '-3 minutes', 'localtime')),
  ('ECHO', 50, datetime('now', '-2 minutes', 'localtime')),
  ('ECHO', 62, datetime('now', '-1 minutes', 'localtime'))
;