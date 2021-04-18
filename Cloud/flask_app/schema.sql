DROP TABLE IF EXISTS bin;
DROP TABLE IF EXISTS fill_level;

--implicit rowid
CREATE TABLE bin (
  bin_name TEXT PRIMARY KEY,
  is_spill INTEGER CHECK(is_spill = 0 OR is_spill = 1),
  is_spill_updated TIMESTAMP DEFAULT (datetime('now','localtime')),
  is_tilt INTEGER CHECK(is_tilt = 0 OR is_tilt = 1),
  is_tilt_updated TIMESTAMP DEFAULT (datetime('now','localtime')),
  xCordinate INTEGER,
  yCordinate INTEGER,
  nearestBin TEXT,
  nearestBin_distance INTEGER
);

--implicit rowid
CREATE TABLE fill_level (
  fill_percent INTEGER NOT NULL CHECK(fill_percent >= 0 AND fill_percent <= 100),
  time_updated TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL,
  bin_name TEXT NOT NULL, 
  tocloud BOOLEAN,
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
INSERT INTO bin (bin_name, is_spill, is_tilt, xCordinate, yCordinate, nearestBIN_distance) 
VALUES
  ('ALPHA', true, false, 4, 20, 11), 
  ('BRAVO', false, true, 15, 22, 29),
  ('CHARLIE', false, false, 28, 18, 14),
  ('DELTA', false, false, 6, 2, 22),
  ('ECHO', false, false, 11, 4, 39)
;

INSERT INTO fill_level (bin_name, fill_percent, time_updated) 
VALUES
  ('ALPHA', 45, datetime('now', '0 seconds', 'localtime')),
  ('ALPHA', 49, datetime('now', '-10 seconds', 'localtime')),
  ('ALPHA', 54, datetime('now', '-20 seconds', 'localtime')),
  ('ALPHA', 58, datetime('now', '-30 seconds', 'localtime')),
  ('ALPHA', 63, datetime('now', '-40 seconds', 'localtime')),
  ('ALPHA', 67, datetime('now', '-50 seconds', 'localtime')),
  ('ALPHA', 71, datetime('now', '-60 seconds', 'localtime')),
  ('ALPHA', 74, datetime('now', '-70 seconds', 'localtime')),
  ('ALPHA', 78, datetime('now', '-80 seconds', 'localtime')),
  ('ALPHA', 81, datetime('now', '-90 seconds', 'localtime')),
  ('ALPHA', 83, datetime('now', '-100 seconds', 'localtime')),
  ('ALPHA', 85, datetime('now', '-110 seconds', 'localtime')),
  ('ALPHA', 87, datetime('now', '-120 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-130 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-140 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-150 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-160 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-170 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-180 seconds', 'localtime')),
  ('ALPHA', 88, datetime('now', '-190 seconds', 'localtime')),
  ('ALPHA', 86, datetime('now', '-200 seconds', 'localtime')),
  ('ALPHA', 84, datetime('now', '-210 seconds', 'localtime')),
  ('ALPHA', 82, datetime('now', '-220 seconds', 'localtime')),
  ('ALPHA', 79, datetime('now', '-230 seconds', 'localtime')),
  ('ALPHA', 76, datetime('now', '-240 seconds', 'localtime')),
  ('ALPHA', 72, datetime('now', '-250 seconds', 'localtime')),
  ('ALPHA', 68, datetime('now', '-260 seconds', 'localtime')),
  ('ALPHA', 64, datetime('now', '-270 seconds', 'localtime')),
  ('ALPHA', 60, datetime('now', '-280 seconds', 'localtime')),
  ('ALPHA', 56, datetime('now', '-290 seconds', 'localtime')),
  ('ALPHA', 51, datetime('now', '-300 seconds', 'localtime')),
  ('ALPHA', 47, datetime('now', '-310 seconds', 'localtime')),
  ('ALPHA', 42, datetime('now', '-320 seconds', 'localtime')),
  ('ALPHA', 38, datetime('now', '-330 seconds', 'localtime')),
  ('ALPHA', 33, datetime('now', '-340 seconds', 'localtime')),
  ('ALPHA', 29, datetime('now', '-350 seconds', 'localtime')),
  ('ALPHA', 25, datetime('now', '-360 seconds', 'localtime')),
  ('ALPHA', 21, datetime('now', '-370 seconds', 'localtime')),
  ('ALPHA', 17, datetime('now', '-380 seconds', 'localtime')),
  ('ALPHA', 14, datetime('now', '-390 seconds', 'localtime')),
  ('ALPHA', 11, datetime('now', '-400 seconds', 'localtime')),
  ('ALPHA', 8, datetime('now', '-410 seconds', 'localtime')),
  ('ALPHA', 5, datetime('now', '-420 seconds', 'localtime')),
  ('ALPHA', 3, datetime('now', '-430 seconds', 'localtime')),
  ('ALPHA', 2, datetime('now', '-440 seconds', 'localtime')),
  ('ALPHA', 1, datetime('now', '-450 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-460 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-470 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-480 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-490 seconds', 'localtime')),
  ('ALPHA', 1, datetime('now', '-500 seconds', 'localtime')),
  ('ALPHA', 3, datetime('now', '-510 seconds', 'localtime')),
  ('ALPHA', 5, datetime('now', '-520 seconds', 'localtime')),
  ('ALPHA', 7, datetime('now', '-530 seconds', 'localtime')),
  ('ALPHA', 10, datetime('now', '-540 seconds', 'localtime')),
  ('ALPHA', 13, datetime('now', '-550 seconds', 'localtime')),
  ('ALPHA', 16, datetime('now', '-560 seconds', 'localtime')),
  ('ALPHA', 20, datetime('now', '-570 seconds', 'localtime')),
  ('ALPHA', 24, datetime('now', '-580 seconds', 'localtime')),
  ('ALPHA', 28, datetime('now', '-590 seconds', 'localtime')),
  ('ALPHA', 32, datetime('now', '-600 seconds', 'localtime')),
  ('ALPHA', 37, datetime('now', '-610 seconds', 'localtime')),
  ('ALPHA', 41, datetime('now', '-620 seconds', 'localtime')),
  ('ALPHA', 46, datetime('now', '-630 seconds', 'localtime')),
  ('ALPHA', 50, datetime('now', '-640 seconds', 'localtime')),
  ('ALPHA', 55, datetime('now', '-650 seconds', 'localtime')),
  ('ALPHA', 59, datetime('now', '-660 seconds', 'localtime')),
  ('ALPHA', 63, datetime('now', '-670 seconds', 'localtime')),
  ('ALPHA', 67, datetime('now', '-680 seconds', 'localtime')),
  ('ALPHA', 71, datetime('now', '-690 seconds', 'localtime')),
  ('ALPHA', 75, datetime('now', '-700 seconds', 'localtime')),
  ('ALPHA', 78, datetime('now', '-710 seconds', 'localtime')),
  ('ALPHA', 81, datetime('now', '-720 seconds', 'localtime')),
  ('ALPHA', 84, datetime('now', '-730 seconds', 'localtime')),
  ('ALPHA', 86, datetime('now', '-740 seconds', 'localtime')),
  ('ALPHA', 88, datetime('now', '-750 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-760 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-770 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-780 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-790 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-800 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-810 seconds', 'localtime')),
  ('ALPHA', 88, datetime('now', '-820 seconds', 'localtime')),
  ('ALPHA', 86, datetime('now', '-830 seconds', 'localtime')),
  ('ALPHA', 84, datetime('now', '-840 seconds', 'localtime')),
  ('ALPHA', 81, datetime('now', '-850 seconds', 'localtime')),
  ('ALPHA', 78, datetime('now', '-860 seconds', 'localtime')),
  ('ALPHA', 75, datetime('now', '-870 seconds', 'localtime')),
  ('ALPHA', 72, datetime('now', '-880 seconds', 'localtime')),
  ('ALPHA', 68, datetime('now', '-890 seconds', 'localtime')),
  ('ALPHA', 64, datetime('now', '-900 seconds', 'localtime')),
  ('ALPHA', 59, datetime('now', '-910 seconds', 'localtime')),
  ('ALPHA', 55, datetime('now', '-920 seconds', 'localtime')),
  ('ALPHA', 51, datetime('now', '-930 seconds', 'localtime')),
  ('ALPHA', 46, datetime('now', '-940 seconds', 'localtime')),
  ('ALPHA', 42, datetime('now', '-950 seconds', 'localtime')),
  ('ALPHA', 37, datetime('now', '-960 seconds', 'localtime')),
  ('ALPHA', 33, datetime('now', '-970 seconds', 'localtime')),
  ('ALPHA', 28, datetime('now', '-980 seconds', 'localtime')),
  ('ALPHA', 24, datetime('now', '-990 seconds', 'localtime')),
  ('ALPHA', 20, datetime('now', '-1000 seconds', 'localtime')),
  ('ALPHA', 17, datetime('now', '-1010 seconds', 'localtime')),
  ('ALPHA', 13, datetime('now', '-1020 seconds', 'localtime')),
  ('ALPHA', 10, datetime('now', '-1030 seconds', 'localtime')),
  ('ALPHA', 7, datetime('now', '-1040 seconds', 'localtime')),
  ('ALPHA', 5, datetime('now', '-1050 seconds', 'localtime')),
  ('ALPHA', 3, datetime('now', '-1060 seconds', 'localtime')),
  ('ALPHA', 1, datetime('now', '-1070 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-1080 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-1090 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-1100 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-1110 seconds', 'localtime')),
  ('ALPHA', 0, datetime('now', '-1120 seconds', 'localtime')),
  ('ALPHA', 2, datetime('now', '-1130 seconds', 'localtime')),
  ('ALPHA', 3, datetime('now', '-1140 seconds', 'localtime')),
  ('ALPHA', 5, datetime('now', '-1150 seconds', 'localtime')),
  ('ALPHA', 8, datetime('now', '-1160 seconds', 'localtime')),
  ('ALPHA', 10, datetime('now', '-1170 seconds', 'localtime')),
  ('ALPHA', 13, datetime('now', '-1180 seconds', 'localtime')),
  ('ALPHA', 17, datetime('now', '-1190 seconds', 'localtime')),
  ('ALPHA', 21, datetime('now', '-1200 seconds', 'localtime')),
  ('ALPHA', 25, datetime('now', '-1210 seconds', 'localtime')),
  ('ALPHA', 29, datetime('now', '-1220 seconds', 'localtime')),
  ('ALPHA', 33, datetime('now', '-1230 seconds', 'localtime')),
  ('ALPHA', 37, datetime('now', '-1240 seconds', 'localtime')),
  ('ALPHA', 42, datetime('now', '-1250 seconds', 'localtime')),
  ('ALPHA', 46, datetime('now', '-1260 seconds', 'localtime')),
  ('ALPHA', 51, datetime('now', '-1270 seconds', 'localtime')),
  ('ALPHA', 55, datetime('now', '-1280 seconds', 'localtime')),
  ('ALPHA', 60, datetime('now', '-1290 seconds', 'localtime')),
  ('ALPHA', 64, datetime('now', '-1300 seconds', 'localtime')),
  ('ALPHA', 68, datetime('now', '-1310 seconds', 'localtime')),
  ('ALPHA', 72, datetime('now', '-1320 seconds', 'localtime')),
  ('ALPHA', 75, datetime('now', '-1330 seconds', 'localtime')),
  ('ALPHA', 79, datetime('now', '-1340 seconds', 'localtime')),
  ('ALPHA', 81, datetime('now', '-1350 seconds', 'localtime')),
  ('ALPHA', 84, datetime('now', '-1360 seconds', 'localtime')),
  ('ALPHA', 86, datetime('now', '-1370 seconds', 'localtime')),
  ('ALPHA', 88, datetime('now', '-1380 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-1390 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-1400 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-1410 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-1420 seconds', 'localtime')),
  ('ALPHA', 90, datetime('now', '-1430 seconds', 'localtime')),
  ('ALPHA', 89, datetime('now', '-1440 seconds', 'localtime')),
  ('ALPHA', 87, datetime('now', '-1450 seconds', 'localtime')),
  ('ALPHA', 86, datetime('now', '-1460 seconds', 'localtime')),
  ('ALPHA', 83, datetime('now', '-1470 seconds', 'localtime')),
  ('ALPHA', 81, datetime('now', '-1480 seconds', 'localtime')),
  ('ALPHA', 78, datetime('now', '-1490 seconds', 'localtime')),

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