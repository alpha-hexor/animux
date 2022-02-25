def parse_log(f):
    
    '''
    function to parse log
    '''
    anime = {}
    anime_last = {}
    names = []
    
    with open(f,'r') as f:
        for line in f.readlines():
            p = line.strip("\n")
            
            if len(p) > 1:
                s = p.split(" ")
                name = s[2]
                name = name.replace(":","")
                names.append(name)
                episode_watched = s[-1].split("-")[-1].split(":")[0]
                last_episode = s[-1].split("-")[-1].split(":")[1]
                
                if episode_watched != last_episode:
                    anime[name] = episode_watched
                    anime_last[name] = last_episode
                else:
                    anime[name] = "finished"
    f.close()
    
    #delete duplicate entries
    n = set(names)
    names = list(n)
    
    #delete already finished animes
    for i in names:
        if anime[i] == "finished":
            names.remove(i)
            
    return anime,anime_last,names