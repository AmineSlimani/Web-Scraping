import requests
from bs4 import BeautifulSoup
import csv

def getUrl(PageNumber) : 
    return f'https://www.jumia.ma/telephone-tablette/?rating=1-5&price_discount=10-100&page={PageNumber}#catalog-listing'


def main(page) :
    global ItemDetails 
    ItemDetails = []
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    ItemCard = soup.find_all('article',{'class':'prd _fb col c-prd'})
    NumberOfItemCard = len(ItemCard)

    def remove_first_last_char(word):
        return word[1:-1]
    
    for i in range(NumberOfItemCard):
        itemInfo = ItemCard[i].find('div',{'class':'info'})
        itemTitle = itemInfo.find('h3',{'class':'name'}).text.strip()
        itemCurrentPrice = itemInfo.find('div',{'class':'prc'}).text.strip()
        itemPrvPrice = itemInfo.find('div',{'class':'s-prc-w'}).find('div',{'class':'old'}).text.strip()
        itemDiscount = itemInfo.find('div',{'class':'s-prc-w'}).find('div',{'class':'bdg _dsct _sm'}).text.strip()
        itemStars = itemInfo.find('div',{'class':'stars _s'}).text.strip()
        itemBuyersNumber = itemInfo.find('div',{'class':'rev'}).contents[1]
        itemBuyersNumber =  remove_first_last_char(itemBuyersNumber)

        ItemDetails.append({"\t Name \t":itemTitle,"\t Current Price\t ":itemCurrentPrice,"\t Previous Price\t ":itemPrvPrice,
                           "\t Discount %\t " :itemDiscount,"\t  Rating \t" :itemStars,"\t Number of Buyers\t " : itemBuyersNumber})

    keys  = ItemDetails[0].keys()
    
    if PageNumber<2 :
        modeOfWriting = "w"
    else : 
        modeOfWriting = "a"

    with open("Electronics_List.ods",modeOfWriting) as file :
        writeOnFile = csv.DictWriter(file,keys)

        if file.tell() == 0:
            writeOnFile.writeheader()   

        writeOnFile.writerows(ItemDetails)
        print(f"Page {PageNumber} Scrapped Successfully!")         

PageNumber = 1
while PageNumber<=50 : 
    url = getUrl(PageNumber)
    page = requests.get(url)
    main(page)
    PageNumber = PageNumber + 1
    
print("The whole Website is Scrapped Successfully!")

