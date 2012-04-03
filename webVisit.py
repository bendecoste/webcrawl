from collections import defaultdict
import re

#used to calculate when reset of visit counters should happen
from datetime import datetime

class webVisit:
	def __init__(self):
		self.urlTable = defaultdict(int) 
		self.CONST_THRESHOLD = 30
		self.timeLapse = None
		self.time = None


	def addUrl(self, url):
		#first remove everything before x.whateverdomain, so we dont count
		#things like funstuff.blogspot.com and other.blogspot.com
		#as different domains
		url = self.parsed_url(url)
		print url
		self.urlTable[url] += 1
		self.manage_time();
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
			self.time = datetime.now().minute
			self.timeLapse = datetime.now().minute
		if self.timeLapse - self.time >= 3 or self.time - self.timeLapse >= 3:
			self.time = datetime.now().minute
			self.timeLapse = datetime.now().minute
			self.reset_list()
			return
		self.timeLapse = datetime.now().minute

	def reset_list(self):
		for urls in self.urlTable:
			self.urlTable[urls] = 0





