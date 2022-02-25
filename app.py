import os
from termcolor import colored
import random
import sys
from codebase.search import *
from codebase.log import *
from codebase.parselog import *
from codebase.getlink import *

#some global things
mpv_executable = "mpv"


#function for color print
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))

#function to return final link
def get_final_link(embade_url):
    qualities,link = generate_links(embade_url)
    
    colored_print("[*]Available Qualities: ")
    for i in range(len(qualities)):
        colored_print("["+str(i+1)+"] "+qualities[i])
    
    opt = int(input("[*]Enter index: "))
    return link[opt-1]

def stream_episode(name,ep_num,last_ep):
    os.system("clear")
    colored_print("[*]Streaming episode: " +name+":"+ep_num)
    
    embade_url = get_embade_link(name,ep_num)
    link = get_final_link(embade_url)
    #print(link)
    command = ' "'+link+'"'
    os.system("nohup "+mpv_executable+command)
    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to start next episode[y/n]: "))
    

        if (opt == "n"):
            exit()
            
        ep_num = int(ep_num)+1
        watch_log(name,str(ep_num),str(last_ep))
        stream_episode(name,str(ep_num),last_ep)
    else:
        
        exit()


#main shit
def main():
    if len(sys.argv) == 1:
        name = input("[*]Enter anime name: ")
        animes,anime_links = search_anime(name)
        
        for i in range(len(animes)):
            colored_print("["+str(i+1)+"] "+animes[i])
        
        #take user input
        opt = int(input("[*]Enter index: "))
        anime_to_watch = anime_links[opt-1]
        
        #get episode list
        first_episode,last_episode = search_episode(anime_to_watch)
        
        colored_print("[*]Available Episode: [" + str(first_episode) + "-"+str(last_episode)+"]")
        
        #take episdode num input
        ep_num = input("[*]Enter episode number: ")
        
        if int(ep_num) >= 0 and int(ep_num) <= last_episode:
            os.system("clear")
            watch_log(anime_to_watch,ep_num,last_episode)
            stream_episode(anime_to_watch,ep_num,last_episode)

    else:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            '''
            --help implementation
            '''
            colored_print("[*]Usage: python app.py --help [for help]")
            colored_print("[*]Usage: python app.py [for normal usage]")
            colored_print("[*]Usage: python app.py --continue_stream [continue watch animes]")
            colored_print("[*]Usage: python app.py --continue_download [continue download animes]")
            
            exit()
        
        
        if sys.argv[1] == "--continue_stream" :

            '''
            --continue_stream implementation
            '''

            #check for log file
            if not os.path.exists("watch_log.txt"):
                colored_print("[*]No watch log found")
                exit()

            anime,anime_last,names=parse_log("watch_log.txt")
            
            #take user input
            colored_print("[*]Continue Watching.........")
            for n in range(len(names)):
                colored_print("["+str(n+1)+"] "+names[n])
            
            x=int(input("[*]Enter index of anime to watch: "))
            anime_to_watch = names[x-1]
            episode_to_watch = int(anime[anime_to_watch]) + 1

            watch_log(anime_to_watch,str(episode_to_watch),anime_last[anime_to_watch])
            stream_episode(anime_to_watch,str(episode_to_watch),anime_last[anime_to_watch])
        
        
 

if __name__ == "__main__":
    main() 
