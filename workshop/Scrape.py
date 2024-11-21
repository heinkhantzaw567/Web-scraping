import requests
from bs4 import BeautifulSoup
#import os
import csv
import pandas as pd

URL= "https://quotes.toscrape.com"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify())

quotes = []
table = soup.findAll("div", attrs={"class": "quote"})

for line in table:
    quote = {}
    quote["Lines"]=line.find("span", attrs={"class":"text"}).string
    quote["Author"]=line.find("small", attrs={"class":"author"}).string
    quotes.append(quote)

getNextQuotes = soup.findAll("li", attrs={"class":"next"})
if not getNextQuotes:
    tailURL =""
else:
    for next in getNextQuotes:
        tailURL  = next.find("a")["href"]


def repeatRequest(tURL):
    fullURL = URL + tURL
    r2 = requests.get(fullURL)
    soup2= BeautifulSoup(r2.content, 'html5lib')
    table2 = soup2.findAll("div", attrs={"class": "quote"})
    # print(soup2.prettify())

    fullQuotes =[]
    for line in table2:
        quote = {}
        quote["Lines"]=line.find("span", attrs={"class":"text"}).string
        quote["Author"]=line.find("small", attrs={"class":"author"}).string
        fullQuotes.append(quote)
    
    getNextQuotes = soup2.findAll("li", attrs={"class":"next"}) 
    if not getNextQuotes:
        return fullQuotes, ""

    for next in getNextQuotes:
        tURL  = next.find("a")["href"]   
        
    return fullQuotes, tURL



while tailURL:
    print(tailURL)
    fullQuotes, tailURL = repeatRequest(tailURL)
    quotes.extend(fullQuotes)









fields =["Lines","Author"]
filename ="quote_list.csv"
f =open(filename, "w", encoding="utf-8")

with f as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=fields)
    writer.writeheader()
    writer.writerows(quotes)

f.close()


df = pd.read_csv("quote_list.csv")
df.to_html("index.html")




