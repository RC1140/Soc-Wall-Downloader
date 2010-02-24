#!/usr/bin/python

#Import Feedparser to read the RSS feeds , URLLIb for downloading etc
import feedparser,urllib2,os.path,sys

def cleanExit():
	print 'No valid parameters were found , usage is socwallDownloader.py autoUpdate'

def autoUpdate():
	#Read in the most recent Socwall uploads
	d = feedparser.parse("http://www.socwall.com/php/rss_RecentWPs.php")

	# Loop through the entries , print each of the entrie that are found , but onl print downloading if the file doesnt exist
	for feed in d.entries:
		print 'Found Link : ' +  feed.link
		currentFile = feed.__str__()[feed.__str__().rfind('/')+1:-2]

		#Get the locations of the slash's for the directory to save into
		firstSlash = feed.link.__str__().find('/',8)
		secondSlash = feed.link.__str__().find('/',firstSlash+1)
		downloadDir = feed.link.__str__()[firstSlash+1:secondSlash]#Get the directory by extracting the data between the slashes
	
		if not os.path.exists(downloadDir):
        		os.makedirs(downloadDir)
	
		if os.path.exists(downloadDir + '/' + currentFile) != True:
			print 'Downloading : '+ downloadDir + '/' + currentFile
			urlFile = urllib2.urlopen(feed.link.__str__())
			output = open(downloadDir + '/' + currentFile,'wb')
			output.write(urlFile.read())
			output.close()


def main(parameters=sys.argv):
	runTypes = {
		'autoUpdate' : autoUpdate}

	runTypes.get(parameters[1].__str__(),cleanExit)()
	print parameters[1]

if __name__ == "__main__":
    main()
