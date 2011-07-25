import os,sys

urls = ["http://www.youtube.com/watch?v=m9l81moVkAU", "http://www.youtube.com/watch?v=xIYXkP5_BIs", "http://www.youtube.com/watch?v=U5nTkRDnVwQ"]
urls2 = ["http://www.novinky.cz/domaci/239621-ve-visnove-na-liberecku-kvuli-povodnim-evakuovali-zeny-a-deti.html?ref=zpravy-dne", "http://www.novinky.cz/domaci/239670-cssd-by-i-pres-ztraty-krajske-volby-vyhrala-pravice-posiluje-a-jde-po-rathovi.html?ref=boxE", "http://www.novinky.cz/domaci/239629-hasici-museli-kvuli-povodni-evakuovat-detsky-tabor.html?ref=boxD"]
texts = ["earth", "earth is great", "home", "home sweet home", "you can't", "you can't take the sky from me"]

UP = 0
DOWN = 1
lastTab = 1
activeTab = 1

def scroll(direction, start = 5):
	print "SET !REPLAYSPEED FAST";
	r = []
	if direction == UP:
		r = range(start,40)
		r.reverse();
	else:
		r = range(start,40)
	for i in r:
		print "CLICK X=0 Y=" + str(i * 50);
		if i % 5 == 0:
			print "WAIT SECONDS=1"
	print "SET !REPLAYSPEED MEDIUM"
	
def head():
	print """VERSION BUILD=7200328 RECORDER=FX"
	SET !TIMEOUT_TAG 15
	SET !ERRORIGNORE YES
	TAB T=1
	TAB CLOSEALLOTHERS
	"""

def switchTab(index):
	activeTab = index
	print "TAB T=" + str(index)

def wait(seconds):
	print "WAIT SECONDS=" + str(seconds)

def openNextYoutubeVideo(index = 4):
	print "TAG POS=" + str(index) + " TYPE=a ATTR=CLASS:video-list-item-link"

def openNextNovinkyArticle(index = 1):
	print "TAG POS=" + str(index) + " TYPE=img ATTR=width:200"

def openURL(url):
	print "URL GOTO=" + url

def openTab():
	global lastTab
	lastTab += 1
	print "TAB OPEN"

def closeTab():
	global lastTab
	lastTab += 1
	print "TAB CLOSE"

def googleSearch(txt):
#TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:f ATTR=NAME:q CONTENT=a
#TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:gs ATTR=NAME:q CONTENT=aaaabbb
#TAG POS=1 TYPE=INPUT:SUBMIT FORM=ID:tsf ATTR=NAME:btnG&&VALUE:Hledat

	print "TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:f ATTR=NAME:q CONTENT=\"" + txt + "\""
	print "TAG POS=1 TYPE=INPUT:SUBMIT FORM=ID:tsf ATTR=NAME:btnG"

def googleSearchContinue(txt):
	print "TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:gs ATTR=NAME:q CONTENT=\"" + txt[:3] + "\""
	wait(1)
	print "TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:gs ATTR=NAME:q CONTENT=\"" + txt + "\""
	print "TAG POS=1 TYPE=INPUT:SUBMIT FORM=ID:tsf ATTR=NAME:btnG"

def openGoogleLink(index):
	print "TAG POS=" + str(38 + index) + " TYPE=A ATTR=HREF:*"

head()
openURL("http://youtube.com")
openTab()
switchTab(2)
openURL("http://novinky.cz")
switchTab(1)

for ii in range(10):
	# switch to youtube tab
	switchTab(1)
	wait(3)
	#openNextYoutubeVideo()
	openURL(urls[0])
	urls=urls[1:] + [urls[0]];
	wait(5)
	scroll(DOWN,15)
	scroll(UP,15)

	# google search
	openTab()
	switchTab(3)
	openURL("http://google.com")
	googleSearch(texts[0])
	wait(2)
	googleSearchContinue(texts[1])
	texts=texts[2:] + [texts[0]] + [texts[1]];
	scroll(DOWN)
	openGoogleLink(30)
	wait(6)
	closeTab()

	# switch to novinky.cz tab
	switchTab(2)
	for i in range(2):
		wait(3)
		openURL(urls2[0])
		urls2=urls2[1:] + [urls2[0]];
		wait(3)
		scroll(DOWN)
		scroll(UP)
