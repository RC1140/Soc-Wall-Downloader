#!/usr/bin/python

#Import Feedparser to read the RSS feeds , URLLIb for downloading etc
import feedparser,urllib2,os.path,sys,urllib, sgmllib

myurl = 'http://img2.socwall.com/Anime/General/'

class HTMLParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks

def cleanExit():
	print 'No valid parameters were found , usage is socwallDownloader.py autoUpdate'

#Create a file locally on the disk and then download the file from the URL provided
def createAndDownload(fileName,URL):
	
	if fileName[0] == '?':
		return

	if not os.path.exists(fileName):
		return

	urlFile = urllib2.urlopen(URL)
	meta = urlFile.info()

	if meta.getheaders("Content-Length")[0] == '0':
		print 'File is empty not downloading'
		return

	print meta.getheaders("Content-Length")[0]

	print 'Starting Download : ' + fileName + ' / ' + URL
	output = open(fileName,'wb')
	output.write(urlFile.read())
	output.close()
	print 'Download Complete'

def extractFileNameFromURL(URLToExtract):
	return URLToExtract.__str__()[URLToExtract.__str__().rfind('/')+1:-2]

def autoUpdate():
	#Read in the most recent Socwall uploads
	d = feedparser.parse("http://www.socwall.com/php/rss_RecentWPs.php")

	# Loop through the entries , print each of the entrie that are found , but onl print downloading if the file doesnt exist
	for feed in d.entries:
		print 'Found Link : ' +  feed.link
		currentFile = extractFileNameFromURL(feed.__str__()) #feed.__str__()[feed.__str__().rfind('/')+1:-2]	
		print currentFile 
		#Get the locations of the slash's for the directory to save into
		firstSlash = feed.link.__str__().find('/',8)
		secondSlash = feed.link.__str__().find('/',firstSlash+1)
		downloadDir = feed.link.__str__()[firstSlash+1:secondSlash]#Get the directory by extracting the data between the slashes
	
		if not os.path.exists(downloadDir):
        		os.makedirs(downloadDir)
	
		#There is a problem with handling URL's with spaces , atm the error is just caught 		
		if os.path.exists(downloadDir + '/' + currentFile) != True:
			try:
				createAndDownload(downloadDir + '/' + currentFile,feed.link.__str__())
			except:
				print 'File Download Failed'
	




#This performs a custom URL download and will ideally download a list of wallpapers from a URL Provided		
def customURLDownload(ExtractionURL=None):
	if ExtractionURL == None:
		print 'Nothing found for custom download you fail'
		ExtractionURL = myurl

	animeLinks = urllib.urlopen(ExtractionURL)
        htmlDats = animeLinks.read()

        # Try and process the page.
        # The class should have been defined first, remember.
        myparser = HTMLParser()
        myparser.parse(htmlDats)

        # Get the hyperlinks.
        customLinks = myparser.get_hyperlinks()
        for links in customLinks:
                print myurl+links
		try:
			createAndDownload(links,myurl+links)
		except:
			print 'Download Failed'


def main(parameters=sys.argv):
	if len(parameters) <= 1:
		cleanExit()
		return

	if len(parameters) >= 3:
		myurl = parameters[2]		
	
	runTypes = {
               	'autoUpdate' : autoUpdate,
		'customDownload' : customURLDownload}

       	runTypes.get(parameters[1].__str__(),cleanExit)()

if __name__ == "__main__":
    main()
