DROP TABLE IF EXISTS bin;

CREATE TABLE bin (
  name TEXT PRIMARY KEY,
  fill_percent INTEGER NOT NULL CHECK(fill_percent >= 0 AND fill_percent <= 100),
  last_updated TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL
);

CREATE TRIGGER bin_last_updated BEFORE UPDATE ON bin
BEGIN
UPDATE bin SET last_updated = (datetime('now','localtime')) WHERE name = old.name;
END;

-- Initialise mock data
INSERT INTO bin (name, fill_percent) 
VALUES
  ('vavet', 15), 
  ('tipov', 45),
  ('popap', 65),
  ('abcde', 90)
;