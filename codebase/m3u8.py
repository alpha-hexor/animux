'''
python code to parse m3u8 quality
'''


from statistics import quantiles
import requests

headers={
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'referer' : 'https://gogoplay.io'
        
}

def get_m3u8_quality(link):
    
    
    partial_link = link[:link.rfind('/')+1]
    
    
    
    
    links = []
    qualities = []
    
    r=requests.get(link,headers=headers)
    s=r.text.replace("#EXTM3U\n","").strip()
    s=s.split("\n")
    
    for i in range(len(s)):
        if i%2 == 1:
            links.append(partial_link+s[i])
        else:
            q=s[i].split(",")[-1].replace("NAME=","").replace('"','')
            qualities.append(q)
    
    return qualities,links

    