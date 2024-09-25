from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

ChannelId = input("Enter Channel ID : ")

url = f"https://www.youtube.com/@{ChannelId}/videos"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

ChannelName = driver.find_element(By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-dynamic-text-view-model/h1/span').text 

last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break 
    last_height = new_height

videos = driver.find_elements(By.CSS_SELECTOR, "ytd-rich-item-renderer")
VideoInfo = []

print(f"Number of Videos : {len(videos)}")

i = 0 

while i < len(videos):
    title = videos[i].find_element(By.XPATH, './/*[@id="video-title"]').text
    when  = videos[i].find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
    vues  = videos[i].find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    link_element = videos[i].find_element(By.XPATH, './/a[@id="video-title-link"]')
    link = link_element.get_attribute("href")
    long = videos[i].find_element(By.XPATH, './/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/div[1]/badge-shape/div').text


    VideoInfo.append({'Song Name': title,'Vues' : vues ,'Date' : when,"Long" : long,"Link" : link})
    
    keys = VideoInfo[0].keys()

    with open(f'{ChannelName}.csv','w') as file :
        writeOnFile = csv.DictWriter(file,keys)
        writeOnFile.writeheader()
        writeOnFile.writerows(VideoInfo) 

    i = i + 1

print(f"The Channel of {ChannelId} has been successfully scraped!")
driver.quit()
