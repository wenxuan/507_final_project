import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os.path
from os import path
#C:\Program Files (x86)\Google\Chrome\Application\chrome.exe

class SteamDiscountItem:
    '''a national site

    Instance Attributes
    -------------------
    title: string
        the title of steam game (e.g. 'National Park', '')
  
    tag: string
    
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
def InfiniteScroll(n=1,tag=None):

    driver = webdriver.Chrome(executable_path=r"C:\Users\19738\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get("https://store.steampowered.com/search/?specials=1&tags=492")

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
        data = InfiniteScroll(numScroll)
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

def Scrap(html,tag=None):
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
        else: positive_rate = None
        

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
        else: rd = None

        # link retrieve
        link = str(item.get("href"))
        #print(link)

        #print("------------------------------------------------")
        i+=1

    
        salesItem = SteamDiscountItem(t, tag, positive_rate, d, op, dp, rd, link)
        AllsalesItem.append(salesItem)
    # caching
    writeItem("Indie.json",AllsalesItem,i)
    return AllsalesItem,i

        
def main():
    #html = InfiniteScroll()
    data = CachePage("steamspecial.html",60)
    tag = 'Indie'
    res,total = Scrap(data,tag)
    for item in res:
        print(item.info())
    #Scrap(html)
    while 1:
        # logic, user interactive part
        comm = input("Please enter [indie, action, adventure, casual] or [quit] to quit: ")
        if comm.strip() == "quit":
            #user enter quit command
            return
        else:   
            # check comm validation / extracting data
            if comm.strip().lower()   == "indie":
                data = CachePage("indie.html",60)
                res,total = Scrap(data,"indie")

            elif comm.strip().lower() == "action":
                pass
            elif comm.strip().lower() == "adventure":
                pass
            elif comm.strip().lower() == "casual":
                pass
            else:
                print("Invalid input.")
                continue
            while 1:
                break
                # view url / plot data
                comm2 = input("Do you want to [view] sales items or [plot] data: ")
                if comm2.strip().lower() == "":
                    pass
                elif comm2.strip().lower() == "":
                    pass
                else:
                    continue

if __name__== "__main__":
   main()
