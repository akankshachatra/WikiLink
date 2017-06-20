from bs4 import BeautifulSoup, SoupStrainer 
import requests
import re

class SearchPhilosophyWiki:

    page_philo=0
    total=0

    def __init__(self):
        self.page={'unavailable': 0}

    def searchPhilosophyLink(self):
        url = 'http://en.wikipedia.org/w/index.php?title=Special:Random' #random url
        r = requests.get(url)
        a = r.text 
        soup = BeautifulSoup(a,"html.parser") #to create BeautifulSoup object from HTML
        print(r.url)
        original_page=r.url # URL of current page
        i=0 # link count to philosophy page

        while (r.url != 'https://en.wikipedia.org/wiki/Philosophy') and i<35: #till the Philosophy page is reached
            count=0
            first_link=None
            while first_link == None: # iterates through each paragraph until it finds it's first link
                if count>(len(soup.select('div#mw-content-text > p'))-1):
                    print "\nNo links found on page.\n"
                    self.page['unavailable']+=1
                    return
                paragraph = soup.select('div#mw-content-text > p')[count] #find paragraph with first real link
                for span in paragraph.find_all("span"):
                    span.replace_with("")#to remove all spans
                para = str(paragraph)
                para = re.sub(r' \(.*?\)', '', para) # remove parantheses
                paragraph = BeautifulSoup(para,"html.parser") #to find first link
                first_link = paragraph.find(href = re.compile('/wiki/'))
                count+=1

            url = 'http://en.wikipedia.org' + first_link.get('href') #final url for next page
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            print(r.url) # prints first link of page to console
            i+=1
        if i==35:
            self.page['unavailable']+=1
        else:
            self.page_philo+=1 # add successful page to
            try:
                self.page[i]+=1 # the number of occurences of path length
            except KeyError: # if key value pair didnt exist
                self.page[i]=1
        self.total+=1
        self.percentage = (self.page_philo/float(self.total))*100
        print "\nCount to get to Philosophy Page: ",i
        print "\n",self.percentage,"percent of all links have gone to Philosophy Page. Total Links:",self.total," Succesful Links:",self.page_philo,"\n"


    def wiki_500(self):
        i=0
        while i <500: # iterate through 500 random links
            self.searchPhilosophyLink() #to get to Philo
            i+=1
            print self.page


search = SearchPhilosophyWiki()
search.wiki_500() #to go through random 500 links
#search.searchPhilosophyLink()
