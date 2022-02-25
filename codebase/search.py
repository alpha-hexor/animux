import requests
from bs4 import BeautifulSoup
import re

#global things
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
main_url = "https://www1.gogoanime.pe/"
anime_links = []
animes = []

#function to search anime
def search_anime(name):
    if len(name) > 1:
        name = name.replace(" ","+")
    search_url = main_url+ "search.html?keyword=" + name
    
    r =requests.get(search_url,headers=headers)
    src = r.content
    soup = BeautifulSoup(src,'lxml')
    hrefs = soup.find_all("p",attrs={'class':'name'})
   #get all the links
    for h in hrefs:
        tags = str(h)
        link = tags.split('/')[2].split('"')[0]
        anime_links.append(link)

    #for the names
    for href in hrefs:
        href = str(href)
        anime_name = re.sub('<[^>]*>', '', href)
        animes.append(str(anime_name))
    
    return animes, anime_links

#function to search episodes
def search_episode(name):
    ep_url = main_url + "category/" + name
    r = requests.get(ep_url, headers=headers)
    src = r.content
    soup = BeautifulSoup(src,'lxml')
    eps = soup.find("a",attrs={'href':'#',"class":"active"}).text
    first_episode = eps.split('-')[0]
    first_episode = int(first_episode)+1

    #for last episode
    try:
        last_episode = eps.split('-')[1]
        last_episode = int(last_episode)
    except:
        last_episode = 1
    return first_episode, last_episode