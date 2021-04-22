import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os.path
from os import path
import plotly
import plotly.express as px
#C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
GLOBAL_URL = {
  "indie":"https://store.steampowered.com/search/?specials=1&tags=492",
  "action":"https://store.steampowered.com/search/?specials=1&tags=19",
  "adventure":"https://store.steampowered.com/search/?specials=1&tags=21",
  "casual":"https://store.steampowered.com/search/?specials=1&tags=597"}

class SteamDiscountItem:
    '''Steam special sales site

    Instance Attributes
    -------------------
    title: string
        the title of steam game (e.g. 'National Park', '')
  
    tag: string
        the tag of steam game
    
    positive rate: string
        the city and state of a national site (e.g. 'Houghton, MI')

    discount rate: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    original price: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')

    release date: string
        the name of a national site (e.g. 'Isle Royale')
    '''
    def __init__(self, title, tag, positive_rate, discount_rate,  original_price, discount_price, release_date, link):
        self.title = title
        self.tag = tag
        self.positive_rate = positive_rate
        self.discount_rate = discount_rate
        self.original_price = original_price
        self.discount_price = discount_price
        self.release_date = release_date
        self.link = link

    def info(self):

        return "({}): {} {} {} {} {}".format(self.title, self.tag,
                                             self.positive_rate,
                                             self.discount_rate,
                                             self.original_price,
                                             self.discount_price,
                                             self.release_date)
    def store(self):
         return [self.title, self.tag,
                self.positive_rate,
                self.discount_rate,
                self.original_price,
                self.discount_price,
                self.release_date,
                self.link]

# start extracting website raw data with cache or feching
def InfiniteScroll(n=1,tag="indie"):

    driver = webdriver.Chrome(executable_path=r"C:\Users\19738\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get(GLOBAL_URL[tag.lower()])

    for i in range(n):
        try:
            # Action scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            break
        except:
            time.sleep(1)

    result = driver.page_source
    driver.close()
    return result

def readCache(fn):

    with open(fn, 'r', encoding="utf-8") as r:
        data = r.read()
    return data

def writeCache(data,fn):
    with open(fn, "w", encoding="utf-8") as f:
        f.write(data)
    f.close()
    return

def CachePage(fn,numScroll):
    path = '/Users/19738/OneDrive/Desktop/SI507/assignment/final project/'+str(fn)
    if os.path.exists(path):
        return readCache(fn)
    else:
        data = InfiniteScroll(numScroll,fn[:-5])
        writeCache(data,fn)
        return data

# caching sales items helper functions
def writeItem(fn,data,total):
    '''
    [
        ["","","",...],     # every list contains title,tag,rates,etc... as strings seperatly
        ["","","",...],
        ...
    ]
    '''
    
    res = [total]
    for item in data:
      #[item.title,item.tag,item.positive_rate,item.discount_rate,item.original_price,item.discount_price,item.release_date,item.link]
        res.append(item.store())
    with open (fn, 'w') as f:
        json.dump(res,f)
    f.close()
    return

def readItem(fn):
    path = '/Users/19738/OneDrive/Desktop/SI507/assignment/final project/'+str(fn)
    if os.path.exists(path):
        with open(fn,"r") as f:
            data = json.load(f)
            f.close()
            return data[0],data[1:]
    else: return -1

# start extracting individual items/sales from a website
def ext_info(item,info_class):
    return item.find(class_=info_class)

def Scrap(html,tag='indie'):
    '''
        param:

        return: list of SteamDiscountItem objects
            [
                SteamDiscountItem,
                SteamDiscountItem,
                ...
            ]
    
    ''' 
    # check if cache already there
    ca = readItem(tag+".json")
    if ca != -1:
        AllsalesItem = []
        for item in ca[1]:
            salesItem = SteamDiscountItem(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            AllsalesItem.append(salesItem)
        return AllsalesItem, ca[0]
    
    # start scraping
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find(id='search_resultsRows')
    items = rows.find_all("a")
    i=0
    AllsalesItem = []

    for item in items:
        # title
        try:
            title = str(ext_info(item,"title"))
            t = title[20:-7].strip()
            
        except:
            continue

        # positive_rate
        p = str(ext_info(item, 'search_review_summary positive'))
        ind = p.find(";")
        positive_rate = p[ind+7:ind+10].strip()
        if positive_rate: 
            if not positive_rate.endswith('%'):
                positive_rate += '%'
        else: positive_rate = ""
        

        # discount rate
        discount_rate = str(ext_info(item, 'col search_discount responsive_secondrow'))
        d = discount_rate[-17:-14].strip('-')

        # original price
        original_price = str(ext_info(item, 'col search_price discounted responsive_secondrow'))
        ind1 = original_price.find("<strike>")
        ind2 = original_price.find("</strike>")
        op = original_price[ind1+8:ind2].strip()

        # discount price
        discount_price = str(ext_info(item, 'col search_price discounted responsive_secondrow'))
        ind3 = discount_price.find("<br/>")
        ind4 = discount_price.find("</div>")
        dp = discount_price[ind3+5:ind4].strip()

        # release date
        release_date = str(ext_info(item, 'col search_released responsive_secondrow'))
        rd = release_date[54:-6].strip()
        if rd: pass
        else: rd = ""

        # link retrieve
        link = str(item.get("href"))
        #print(link)

        #print("------------------------------------------------")
        i+=1

    
        salesItem = SteamDiscountItem(t, tag, positive_rate, d, op, dp, rd, link)
        AllsalesItem.append(salesItem)
    # caching
    writeItem(str(tag)+".json",AllsalesItem,i)
    return AllsalesItem,i

def printSalesItems(data,total,tag,limit=50,startwith=0):
    # header
    print("--------------------------------------------------------")
    print("#{} has {} number of sales items in the list#".format(str(tag).capitalize(),total))
    print("--------------------------------------------------------")
    print("{:6} {:40} {:6} {:13} {:13} {:13} {:13} {:13}". format("","title","tag","positive_rate","discount_rate","original_price", "discount_price", "release_date"))

    for i in range(startwith,startwith+limit):
        if i >= len(data): return 0
        item = data[i]
        print("[{:4}] {:.40s} {:6} {:13} {:13} {:13} {:13} {:13}".format(i,item.title.ljust(40),item.tag,
        item.positive_rate,
        item.discount_rate,
        item.original_price,
        item.discount_price,
        item.release_date))
    return 1

def printSalesItemsWithLimitAndControlUnit(data,total,tag,limit = 50):
    startwith = 0
    repeat = 1
    while repeat:
        repeat = printSalesItems(data,total,tag,limit,startwith)
        
        while 1:
            # user input
            comm3 = (input("Choose a number you want to see its url or [next] to see next set of items, or [exit] return to view/plot: "))
            if comm3.strip().lower() == "exit": return
            elif comm3.strip().lower() == "next": break
            if startwith <= int(comm3) and int(comm3) < startwith+limit and int(comm3) < len(data):
                # provide URL
                comm3 = int(comm3)
                #asdasdasdasdas?????????????
                print("this is your url")
                return
            else:
                print("Invalid input, please choose again")
                continue
            # validating input

        startwith += limit

def viewURL(data,total,tag):
    limit = 50
    # format printing and selecting
    printSalesItemsWithLimitAndControlUnit(data,total,tag,limit)


def barPlot():
    pass

def scatterPlot(res,total):

    tup = []
    for item in res:
        if item.discount_price and item.discount_rate:
            if item.discount_price.strip("$") == "Free":
                dis_price = "0"
            else: dis_price = item.discount_price
            tup.append([int(float(dis_price.strip("$"))),
                        int(item.discount_rate.strip("%"))]
                      )
        continue

    tup.sort()

    x,y = ["$"+str(i[0]) for i in tup], [str(i[1])+"%" for i in tup]
    fig = px.scatter(x, y)
    fig.show()


def main():
    # start doing logic with user prompt
    while 1:
        # logic, user interactive part
        comm = input("Please enter [indie, action, adventure, casual] or [exit] to exit program: ")
        if comm.strip() == "exit":
            #user enter quit command
            return
        else:   
            # prepare for extraction
            res,total,tag = {},-1,"lalala"
            # check comm validation / extracting data
            if comm.strip().lower()   == "indie":
                data = CachePage("indie.html",60)
                res,total = Scrap(data,"indie")
                tag = "indie"
            elif comm.strip().lower() == "action":
                data = CachePage("action.html",60)
                res,total = Scrap(data,"action")
                tag = "action"
            elif comm.strip().lower() == "adventure":
                data = CachePage("adventure.html",60)
                res,total = Scrap(data,"adventure")
                tag = "adventure"
            elif comm.strip().lower() == "casual":
                data = CachePage("casual.html",60)
                res,total = Scrap(data,"casual")
                tag = "casual"
            else:
                print("Invalid input.")
                continue
            while 1:
                # view url / plot data
                comm2 = input("Do you want to [view] sales items or [plot] data, or you can [back] to back to last step, or [exit] to exit the program: ")
                if comm2.strip().lower() == "back": break
                if comm2.strip().lower() == "exit": return
                # valid command
                if comm2.strip().lower() == "plot":
                    comm3 = input("Do you want a [bar] plot or a [scatter] plot? Or you can [back] to back to last step, or [exit] to exit the program:")
                    if comm3.strip().lower() == "bar":
                        barPlot()
                    elif comm3.strip().lower() == "scatter":
                        scatterPlot(res,total)
                    elif comm3.strip().lower() == "back": break
                    elif comm3.strip().lower() == "exit": return
                    else:
                        print("Invalid input.")
                        continue
                    
                elif comm2.strip().lower() == "view":
                    viewURL(res,total,tag)
                    continue
                else:
                    print("Invalid input.")
                    continue

if __name__== "__main__":
   main()
