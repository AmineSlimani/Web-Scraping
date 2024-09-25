import requests
from bs4 import BeautifulSoup
import csv

def getData():
    global year,month,day
    year = input(" Enter year : ")
    month = input(" Enter month : ")
    day = input(" Enter day : ")

def getUrl(year,month,day):
    return (f'https://www.yallakora.com/match-center/?date={year}-{month}-{day}')

def main(page):
    MatchInfo = []
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    Champions = soup.find_all('div',{'class':'matchCard'})
    NumberOfChampions = len(Champions)

    for i in range(NumberOfChampions):
        ChampionTitle = Champions[i].find("h2").text.strip()
        
        Matches = Champions[i].find_all('div',{'class':'liItem'})
        NumberOfMatches = len(Matches)

        for j in range(NumberOfMatches):
            
            teamA = Matches[j].find('div',{'class':'teamA'}).find("p").text.strip()
            teamB = Matches[j].find('div',{'class':'teamB'}).find("p").text.strip()
            MatchStatus =  Matches[j].find('div',{'class':'matchStatus'}).find('span').text.strip()
            MResult = Matches[j].find('div',{'class':'MResult'})
            score1 = MResult.contents[1].text.strip()
            score2 = MResult.contents[5].text.strip()
            Score = f'\t {score1} - {score2} \t'
            MatchTiming = MResult.contents[7].text.strip()
            
            MatchInfo.append({"البطولة":ChampionTitle,"الفريق الأول":teamA,"الفريق الثاني":teamB,
                              "النتيجة":Score,"توقيت":MatchTiming ,"حالة المباراة":MatchStatus })
                    
    keys = MatchInfo[0].keys()

    with open(f"{year}-{month}-{day}.ods","w") as file:
        writeOnFile = csv.DictWriter(file,keys)
        writeOnFile.writeheader()
        writeOnFile.writerows(MatchInfo)
        print(" File Created Successfully! ")

getData()
url = getUrl(year,month,day) 
page = requests.get(url)
main(page)
#By Amine Slimani
