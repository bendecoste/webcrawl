import MySQLdb as mdb
from webVisit import webVisit

class DB_comms:

	def __init__(self):
		self.connection = mdb.connect(host="192.168.0.6", user="bendeco", passwd = "password", db = "crawlbot")
		self.cursor = self.connection.cursor()	
		self.visit = webVisit()	

	def insert(self, url, title):
		query = "INSERT IGNORE into Indexed (title, url) values"
		query += "(\'" + mdb.escape_string(title) + "\', \'" 
		query += mdb.escape_string(url) + "\')"	
		self.cursor.execute(query)

	def insert_auth(self, url, title):
		query = "SELECT COUNT(domain) FROM Auth WHERE domain = '"
		query += "" + mdb.escape_string(url) +"'"				
		self.cursor.execute(query)
		num = self.cursor.fetchone()		

		if num[0] > 0:
			query = "UPDATE Auth SET counter=counter+1 WHERE "
			query += "domain = '" + mdb.escape_string(url) + "'"
			self.cursor.execute(query)		
		else:
			query = "INSERT INTO Auth (domain, title) "
			query += "VALUES('" + mdb.escape_string(url) + "', '" + mdb.escape_string(title) + "')"
			self.cursor.execute(query)
