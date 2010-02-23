import feedparser,urllib2,os.path

d = feedparser.parse("http://www.socwall.com/php/rss_RecentWPs.php")

for feed in d.entries:
	print 'Found Link : ' +  feed.link
	currentFile = feed.__str__()[feed.__str__().rfind('/')+1:-2]
	firstSlash = feed.link.__str__().find('/',8)
	secondSlash = feed.link.__str__().find('/',firstSlash+1)
	downloadDir = feed.link.__str__()[firstSlash+1:secondSlash]
	
	if not os.path.exists(downloadDir):
        	os.makedirs(downloadDir)
	
	if os.path.exists(downloadDir + '/' + currentFile) != True:
		print 'Downloading : '+ downloadDir + '/' + currentFile
		urlFile = urllib2.urlopen(feed.link.__str__())
		output = open(downloadDir + '/' + currentFile,'wb')
		output.write(urlFile.read())
		output.close()

