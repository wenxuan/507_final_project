import sqlite3
import os.path
from os import path
import json

def create():
    
    # file exist check
    path = '/Users/19738/OneDrive/Desktop/SI507/assignment/final project/steamspecialsales.db/'
    if os.path.exists(path):
        pass
    else:
        
        #create database
        con = sqlite3.connect('steamspecialsales.db')
        cur = con.cursor()
        #create table
        cur.execute('''CREATE TABLE MainSite
                (tag text not null, URL text not null)''')
        cur.execute('''CREATE TABLE IndieSite
                (title text not null, tag text not null, positiveRate text, discountRate text, originalPrice text,discountPrice text, realeaseDate text, url text, key integer NOT NULL PRIMARY KEY)''')
        cur.execute('''CREATE TABLE CasualSite
                (title text not null, tag text not null, positiveRate text, discountRate text, originalPrice text,discountPrice text, realeaseDate text, url text, key integer NOT NULL PRIMARY KEY)''')
        cur.execute('''CREATE TABLE AdventureSite
                (title text not null, tag text not null, positiveRate text, discountRate text, originalPrice text,discountPrice text, realeaseDate text, url text, key integer NOT NULL PRIMARY KEY)''')
        cur.execute('''CREATE TABLE ActionSite
                (title text not null, tag text not null, positiveRate text, discountRate text, originalPrice text,discountPrice text, realeaseDate text, url text, key integer NOT NULL PRIMARY KEY)''')
        #read json file
        data1=[]
        data2=[]
        data3=[]
        data4=[]
        with open("indie.json","r") as f:
            data1 = json.load(f)
            f.close()
        with open("casual.json","r") as f:
            data2 = json.load(f)
            f.close()
        with open("adventure.json","r") as f:
            data3 = json.load(f)
            f.close()
        with open("action.json","r") as f:
            data4 = json.load(f)
            f.close()


        cur.execute('''INSERT INTO MainSite VALUES ("Indie", "https://store.steampowered.com/search/?specials=1&tags=492") ''')
        cur.execute('''INSERT INTO MainSite VALUES ("Casual", "https://store.steampowered.com/search/?specials=1&tags=597") ''')
        cur.execute('''INSERT INTO MainSite VALUES ("Adventure", "https://store.steampowered.com/search/?specials=1&tags=21") ''')
        cur.execute('''INSERT INTO MainSite VALUES ("Action", "https://store.steampowered.com/search/?specials=1&tags=19") ''')

    # Insert a row of data
    # for loop
    for i in range(1,len(data1)):
        comm = '''INSERT INTO IndieSite VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(data1[i][0].replace("\'"," "),data1[i][1],data1[i][2],data1[i][3],data1[i][4],data1[i][5],data1[i][6],data1[i][7],i)
        cur.execute(comm)

    for i in range(1,len(data2)):
        comm = '''INSERT INTO CasualSite VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(data2[i][0].replace("\'"," "),data2[i][1],data2[i][2],data2[i][3],data2[i][4],data2[i][5],data2[i][6],data2[i][7],i)
        cur.execute(comm)

    for i in range(1,len(data3)):
        comm = '''INSERT INTO AdventureSite VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(data3[i][0].replace("\'"," "),data3[i][1],data3[i][2],data3[i][3],data3[i][4],data3[i][5],data3[i][6],data3[i][7],i)
        cur.execute(comm)

    for i in range(1,len(data4)):
        comm = '''INSERT INTO ActionSite VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(data4[i][0].replace("\'"," "),data4[i][1],data4[i][2],data4[i][3],data4[i][4],data4[i][5],data4[i][6],data4[i][7],i)
        cur.execute(comm)


        
        
        
    # Save (commit) the changes
    con.commit()

    # Close connection
    con.close()





create()
