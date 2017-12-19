#Eric Mok, Siddhant Singh, Ruotong Wang
#COMP 123 Lian Duan
# In this program we do web-scraping from Yelp.com to build a database
# of Chinese Restaurants in the Twin Cities
#Requires BeautifulSoup to work.


from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import json
import csv



yelpRestList=[]


def restCompile():
    """Here we compile a list of Chinese restaurants in the Twin Cities, the details of which we want to scrape and put into our database.
        We read the urls through python's urllib module"""
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/little-szechuan-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/rainbow-chinese-restaurant-and-bar-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/hong-kong-noodle-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/jun-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/red-dragon-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/tasty-pot-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/lepot-chinese-hotpot-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/mandarin-kitchen-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/pagoda-minneapolis-5"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/cheng-heng-restaurant-saint-paul"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/yangtze-st-louis-park"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/keefer-court-bakery-and-caf%C3%A9-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/lao-sze-chuan-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/grand-szechuan-bloomington-3"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/mandarin-kitchen-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/new-beijing-eden-prairie-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/caf%C3%A9-99-saint-paul-3"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/peking-garden-saint-paul"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/grand-shanghai-restaurant-saint-paul"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/shuang-cheng-restaurant-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/cathay-chow-mein-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/sidewalk-kitchen-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/xin-wong-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/kowloon-restaurant-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/tea-house-chinese-restaurant-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/szechuan-spice-minneapolis"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/hong-kong-noodle-minneapolis-2"))
    yelpRestList.append(urllib.request.urlopen("https://www.yelp.com/biz/mei-inn-chinese-foods-minneapolis"))


listDict=[]
def scraping():
    """This function takes in no parameters. When it is called, it scrapes the urls found in the yelpRestList, which is a global variable.
        When it comes across the part of the URL which contains the data we want(in the url, the data is contained in a dictionary in json), it
        saves the data in a csv file where each key of the dictionary becomes a column title and each new row entry is a new restaurant."""
    for i in range(len(yelpRestList)):
        yelpHtml = yelpRestList[i].read()
        yelpRestList[i].close()
        soup = BeautifulSoup(yelpHtml, "lxml")
        yelpRest = soup.find_all("script", type="application/ld+json")
        for links in yelpRest:
            listDict.append(json.loads(links.contents[0]))
        with open('names.csv', 'w', newline='',encoding='utf-8') as csvfile:
            fieldnames = ['review', 'servesCuisine','@type','aggregateRating','image','address','name','@context','telephone','priceRange']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listDict)

if __name__ == '__main__':
    restCompile()
    scraping()
#to test the scraping function, we manually open the csv file we have created and go through it to ensure scraping happened properly.
