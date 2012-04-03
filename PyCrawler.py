import sys
import traceback
import re
import urllib2
import urlparse
from webVisit import webVisit
from DB_comms import DB_comms

#for checking robots.txt files
import robotparser as rbp

tocrawl = set([sys.argv[1]])
crawled = set([])
rp = rbp.RobotFileParser()
keywordregex = re.compile('<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
crawlregex = re.compile

#call webVisit class -- used to keep track of visited websites
visit = webVisit()
#DB manager
mdb = DB_comms()
count = 0;

while 1:
	try:
		crawling = tocrawl.pop()
		print crawling
	except KeyError:
		raise StopIteration
	url = urlparse.urlparse(crawling)

	#get website location on www
	site_url = url.netloc

	site_url += "/robots.txt"
	
	
	try:
		rp.set_url("http://" + site_url)
		rp.read()
		if rp.can_fetch("*", crawling):
			if visit.can_query(url.netloc):
				response = urllib2.urlopen(crawling)
				visit.addUrl(url.netloc)
			else:
				print 'too many requests to website, skipping'
				continue
		else:
			print "YOU CAN'T GO HERE"
			continue
	except:
		continue
	msg = response.read()
	startPos = msg.find('<title>')
	if startPos != -1:
		endPos = msg.find('</title>', startPos+7)
		if endPos != -1:
			title = msg[startPos+7:endPos]
			mdb.insert(crawling, title)	
	keywordlist = keywordregex.findall(msg)
	if len(keywordlist) > 0:
		keywordlist = keywordlist[0]
		keywordlist = keywordlist.split(", ")
		#print keywordlist
	links = linkregex.findall(msg)
	crawled.add(crawling)
	for link in (links.pop(0) for _ in xrange(len(links))):
		if link.startswith('/'):
			link = 'http://' + url[1] + link
		elif link.startswith('#'):
			link = 'http://' + url[1] + url[2] + link
		elif not link.startswith('http'):
			link = 'http://' + url[1] + '/' + link
		if link not in crawled:
			tocrawl.add(link)
