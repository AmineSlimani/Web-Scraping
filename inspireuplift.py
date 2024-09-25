import requests
from bs4 import BeautifulSoup
import csv

def getUrl(PageNumber) : 
    return f'https://www.inspireuplift.com/c/home-garden-tools/kitchen-and-dining?page={PageNumber}'

def format_number(word):
    if '.' in word:
        return word
    else:
        if len(word) > 2:
            formatted_word = word[:-2] + '.' + word[-2:]
        else:
            formatted_word = word
        return formatted_word

def main(page) :
    global ItemDetails 
    ItemDetails = []
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    ItemCard = soup.find_all('div',{'class':'primary-card-container'})
    NumberOfItemCard = len(ItemCard)


    for i in range(NumberOfItemCard):
        itemInfo = ItemCard[i].find('div',{'class':'card-inner-wrapper block'})
        itemTitle = itemInfo.find('h2',{'class':'card-title overflow-hidden card-title-one-line'}).text.strip()
        itemCurrentPrice = itemInfo.find('div',{'class':'new-price-container'}).text.strip().replace("Now","").replace("$","")
        itemCurrentPrice = format_number(itemCurrentPrice)
        itemStore= itemInfo.find('div',{'class':'seller-name-container'}).find('span').text.strip()

        ItemDetails.append({"\t Name \t":itemTitle,"\t Current Price $\t ":itemCurrentPrice,"\t Store \t ":itemStore})

    keys  = ItemDetails[0].keys()
    
    if PageNumber<2 :
        modeOfWriting = "w"
    else : 
        modeOfWriting = "a"

    with open("Kitchen_Tools.ods",modeOfWriting) as file :
        writeOnFile = csv.DictWriter(file,keys)

        if file.tell() == 0:
            writeOnFile.writeheader()   

        writeOnFile.writerows(ItemDetails)
        print(f"Page {PageNumber} Scrapped Successfully!")        

PageNumber = 1
while PageNumber<=31 : 
    url = getUrl(PageNumber)
    page = requests.get(url)
    main(page)
    PageNumber = PageNumber + 1
    
print("The whole Website is Scrapped Successfully!")

