import requests
from bs4 import BeautifulSoup
import csv


def getUrl(pageNumber):
    return (f'https://www.lepiceriefineandco.ma/alcools/page{pageNumber}.html?limit=36&mode=grid')

def main(page):
    DrinkInfo = []
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    DrinkCard = soup.find_all('div',{'class':'sg-col-inner'})
    NumberOfDrinkCard = len(DrinkCard)

    for i in range(NumberOfDrinkCard):
        DrinkTitle = DrinkCard[i].find('h4').find('a',{'class':'title'}).text.strip()
        DrinkPrice = DrinkCard[i].find('div',{'class':'product-block-price'}).find('strong').text.strip()
        
        DrinkInfo.append({"Name": DrinkTitle, "Price": DrinkPrice})

    keys  = DrinkInfo[0].keys()
    
    if PageNumber<2 :
        modeOfWriting = "w"
    else : 
        modeOfWriting = "a"

    with open("Alcohols_List.csv",modeOfWriting) as file :
        writeOnFile = csv.DictWriter(file,keys)

        if file.tell() == 0:
            writeOnFile.writeheader()   

        writeOnFile.writerows(DrinkInfo)
        print(f"Page {PageNumber} Scrapped Successfully!")      
 
PageNumber = 1
while PageNumber<6 : 
    url = getUrl(PageNumber)
    page = requests.get(url)
    main(page)
    PageNumber = PageNumber + 1

print(f"The whole website Scrapped Successfully!")
#By Amine Slimani