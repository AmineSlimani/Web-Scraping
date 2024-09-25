from helium import *
from bs4 import BeautifulSoup
import lxml
import csv
import time
import random

global ProductInfo

ProductInfo = []

def getURL(pageNumber):
    return f"https://www.amazon.fr/s?i=computers&rh=n%3A429879031&s=popularity-rank&fs=true&page={pageNumber}&low-price=16&high-price="

def main(browser) :
  
    soup = BeautifulSoup(browser.page_source,'lxml')
    ProductCard  = soup.find_all("div",{"class":"sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"})
    
    i = 0
    while(i<1):
        try :
            ProductTitle = ProductCard[i].find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text.strip()
            ProductPrice = ProductCard[i].find('div',{'data-cy' : 'price-recipe'}).find('span',{'class':'a-offscreen'}).text.strip()
            ProductInfo.append({'\n Title \n' : ProductTitle,'\n Price \n' : ProductPrice})
        except :
            pass 
        i = i + 1 

    keys = ProductInfo[0].keys()
    with open("Electronics_List.ods","a") as file :
        writeOnFile = csv.DictWriter(file,keys)

        if file.tell() == 0:
            writeOnFile.writeheader()   

        writeOnFile.writerows(ProductInfo)
        print(f"Page {pageNumber} Scrapped Successfully!") 

pageNumber = 1 
while pageNumber <= 248 :
    url = getURL(pageNumber)
    browser = start_chrome(url, headless=True)
    main(browser)
    time.sleep(random.randint(1, 10))
    pageNumber = pageNumber + 1
    
print("The whole Website has been successfully scrapsped!")