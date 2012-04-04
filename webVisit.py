from collections import defaultdict
import re

#used to calculate when reset of visit counters should happen
from datetime import datetime

class webVisit:
	def __init__(self):
		self.urlTable = defaultdict(int) 
		self.CONST_THRESHOLD = 3
		self.timeLapse = None
		self.time = None


	def addUrl(self, url):
		#first remove everything before x.whateverdomain, so we dont count
		#things like funstuff.blogspot.com and other.blogspot.com
		#as different domains
		url = self.parsed_url(url)
		self.urlTable[url] += 1
		self.manage_time()
		print self.urlTable

			
	def parsed_url(self, url):
		new = re.split('\.', url)
		new = new[len(new)-2] + '.' + new[len(new)-1]
		return new

	def can_query(self, url):
		url = self.parsed_url(url)
		#if self.urlTable[url] < self.CONST_THRESHOLD:
		#	return True
		#return False
		return self.urlTable[url] < self.CONST_THRESHOLD
	
	def manage_time(self):
		if self.time is None:
			self.time = datetime.now().second
			self.timeLapse = datetime.now().second
		if self.timeLapse - self.time >= 5 or self.time - self.timeLapse >= 5:
			self.time = datetime.now().second
			self.timeLapse = datetime.now().second
			self.reset_list()
			print 'reset list'
			return
		self.timeLapse = datetime.now().second

	# reset entries back down to zero after enough time has passed to query again
	# if an item is at zero (has not be queried this round) delete from list
	# this prevents the list from growing overly large
	def reset_list(self):
		for urls, count in self.urlTable.items():
			if count == 0:
				del self.urlTable[urls]
		for urls in self.urlTable:
			self.urlTable[urls] = 0




