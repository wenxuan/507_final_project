# 507_final_project

In this project we need lots of packages in our program.

Packages for infinite scrolling:
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Option

Packages for Scraping:
from bs4 import BeautifulSoup 
from urllib.parse import urljoin

Packages for save file(caching):
import json
import os.path
from os import path

Packages for plot(Plotly):
import plotly
import plotly.express as px
import pandas
import plotly.graph_objects as go

Package for open URL directly:
import webbrowser

In this program I provide four datasets from four Steam special sales in different tags. 
The four tags are: Indie, Action, Adventure, and Casual. 
Users can fist choose a tag that they like, the program will automatically download the data into a HTML and a JSON file to evaluate the speed of the program.
Then users can choose to see the data or plot the data of the tag they choose.
If they choose to see the data, they can see the title, tag, positive rate, discount rate, original price, discount price and release date of the games. Each game will have a number before the data. By entering the number, the program will automatically open a browser for user to see the website of the game they choose.
If they choose to plot the data, they will be given two options. First is Bar plot, the other is Scatter plot. After selecting bar or scatter, user can automatically open a browser to see the plot. Since there are four different datasets and two different plot types, users can give 8 different plots in this program. 

