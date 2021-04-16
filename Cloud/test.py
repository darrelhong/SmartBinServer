import sqlite3
import time

name = "Cloud"

	
def getNearestBin(queryBin):
	c1 = conn.cursor()
	# sql="SELECT name FROM flaskr.sql.sqlite_master WHERE type='table'"
	c1.execute("SELECT nearestBin, nearestBin_distance FROM bin WHERE bin_name = ?", ["ALPHA"])
	# c1.execute
	data = c1.fetchone()
	targetBin = str(data[0])
	targetDistance = str(data[1])
	return "" + targetBin + ", " + targetDistance  

def test(queryBin):
	c1 = conn.cursor()
	c1.execute("SELECT * FROM (SELECT *, max(time_updated) AS time_updated FROM fill_level NATURAL JOIN bin GROUP BY bin_name) WHERE fill_percent < 80 AND bin_name IS NOT ? ORDER BY nearestBIN_distance asc LIMIT 1", ["ALPHA"])
	data = c1.fetchone()
	print(str(data[2]))
	print(str(data[9]))


try:
	conn = sqlite3.connect("./instance/flaskr.sqlite")
	print(test("ALPHA"))


except KeyboardInterrupt:
	print("Program terminated!")