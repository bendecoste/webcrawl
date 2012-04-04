import sys
import traceback
import re
import urllib2
import urlparse
from Queue import Queue
from webVisit import webVisit
from DB_comms import DB_comms

#checking forrobots.txt files
import robotparser as rbp

tocrawl = Queue()
tocrawl.put(sys.argv[1])
tocrawl.put(sys.argv[2])
tocrawl.put(sys.argv[3])

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
		crawling = tocrawl.get()
		#print crawling
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
				print 'ok'
				visit.addUrl(url.netloc)
			else:
				print 'too many requests to website, skipping'
				#update times at this point to request again asap
				visit.manage_time()
				#add back to list of things to query, get it later
				tocrawl.put(crawling)	
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
	links = linkregex.findall(msg)
	crawled.add(crawling)
	for link in (links.pop(0) for _ in xrange(len(links))):
		if link.startswith('/'):
			link = 'http://' + url[1] + link
		elif link.startswith('#'):
			link = 'http://' + url[1] + url[2] + link
		elif not link.startswith('http'):
			link = 'http://' + url[1] + '/' + link
#		link_from_page = urlparse.urlparse(link)
#		link_from_page = visit.parsed_url(link_from_page.netloc)
#		on_page = urlparse.urlparse(crawling)
#		if not link_from_page is visit.parsed_url(on_page.netloc):
#			mdb.insert_auth(link_from_page, title)
		if link not in crawled:
			tocrawl.put(link)
