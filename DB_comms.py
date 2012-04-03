import MySQLdb as mdb

class DB_comms:

	def __init__(self):
		self.connection = mdb.connect(host="192.168.0.6", user="bendeco", passwd = "password", db = "crawlbot")
		self.cursor = self.connection.cursor()	
	
	def insert(self, url, title):
		query = "INSERT IGNORE into Indexed values"
		query += "(\'" + mdb.escape_string(title) + "\', \'" 
		query += mdb.escape_string(url) + "\')"	
		self.cursor.execute(query)
