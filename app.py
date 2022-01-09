import base64
import json
import yarl
from Cryptodome.Cipher import AES
import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
import random
import os
from datetime import date
from datetime import datetime

#global shit
anime_links = []
animes = []

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

main_url = "https://www3.gogoanime.cm/"
mpv_executable = "mpv"

#function for color print
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))
#padding
def pad(data):
    length = 16-(len(data)%16)
    return data+chr(length)*length

#function for get final shit link
def parse_url(embade_url):
    qualities = []
    links=[]
    s = b"257465385929383"b"96764662879833288"
    p_url = yarl.URL(embade_url)
    next_host = "https://{}/".format(p_url.host)
    encrypted_ajax = base64.b64encode(AES.new(s, AES.MODE_CBC, iv=b'4206913378008135').encrypt(pad(p_url.query.get('id').replace('%3D', '=')).encode()))
    c=(requests.get(
        "{}encrypt-ajax.php".format(next_host),
        params={
            'id':encrypted_ajax.decode(),
            'time':'69420691337800813569'
        },
        headers={'x-requested-with':'XMLHttpRequest'}
    ))
    j = json.loads(c.text)
    for i in range(4):
        try:
            link = j['source'][i]['file']
            links.append(link)
            q = j['source'][i]['label']
            qualities.append(q)
        except:
            pass
    colored_print("[*]Availabel qualities")
    for i in range(len(qualities)):
        colored_print("["+str(i+1)+"]"+qualities[i])
    x = int(input("[*]Enter Index: "))
    x -= 1
    return links[x]



#function to search anime
def search_anime(name):
    if len(name) > 1:
        name = name.replace(" ","-")
    search_url = main_url + "//search.html?keyword="+name
    r = requests.get(search_url,headers=headers)
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

#function to search last and first episode
def search_episode(name):
    ep_url = main_url + "/category/"+name

    k = requests.get(ep_url,headers=headers)
    src2 = k.content
    soup2 = BeautifulSoup(src2,'lxml')
    eps = soup2.find("a",attrs={'href':'#',"class":"active"}).text
    first_episode = eps.split("-")[0]
    first_episode = int(first_episode)+1
    try:
        last_episode = eps.split("-")[1]
        last_episode = int(last_episode)
    except:
        last_episode = 1
    return(first_episode,last_episode)

#create a log
def create_log(name,ep_number):
    current_date = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open("watch_log.txt","a") as f:
        f.write("["+str(current_date) + ":" + current_time + " ] Starting " + name+": episode-"+ep_number+"\n")
    f.close()

#get embade url
def get_embade_link(name,ep_num):
    link = main_url + "/"+name+"-episode-"+ep_num
    try:
        m = requests.get(link,headers=headers)
    except:
        main_url + "/"+name+"-episode-0"
        m=requests.get(link,headers=headers)
    src3 = m.content
    soup3 = BeautifulSoup(src3,'lxml')
    
    for item in soup3.find_all('a', attrs={'href':'#',"rel":"100",'data-video' : True}):
        url = str(item['data-video'])
    url = "https:" + url
    return url

def stream_episode(name,ep_num,last_ep):
    os.system("clear")
    colored_print("[*]Streaming episode: " +name+":"+ep_num)
    
    embade_url = get_embade_link(name,ep_num)
    link = parse_url(embade_url)
    #print(link)
    command = ' "'+link+'"'
    os.system("nohup "+mpv_executable+command)
    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to start next episode[y/n]: "))
    

        if (opt == "y"):
            
            ep_num = int(ep_num)+1
            create_log(name,str(ep_num))
            stream_episode(name,str(ep_num),last_ep)
        else:
            exit()
    else:
        exit()


#main shit
def main():
    try:
        #search the anime
        name = input("[*]Enter anime name: ")
        search_anime(name)
        
        #print all the names
        for i in range(len(animes)):
            colored_print("["+str(i+1)+"] " + animes[i])

        #Take input
        s = int(input("[*]Enter index number to watch: "))
        anime_to_watch = anime_links[s-1]

        #get all episode numbers
        first_ep,last_ep = search_episode(anime_to_watch)
        colored_print("[*]Available Episode: [" + str(first_ep) + "-"+str(last_ep)+"]")
        episode_num = input("[*]Enter episode number: ")

        if((int(episode_num) >= 0) and (int(episode_num) <= last_ep)):
            os.system("clear")
            create_log(anime_to_watch,episode_num)
            stream_episode(anime_to_watch,episode_num,last_ep)
        else:
            print("[*]Invalid Episode number")
    except Exception as e:
        print(e)
main()
