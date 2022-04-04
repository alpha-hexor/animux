'''
python code to parse m3u8 quality
'''

import requests
import regex

#regex 
start_regex = regex.compile(r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)")
res_regex = regex.compile(r"RESOLUTION=\d+x(\d+)")

headers={
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'referer' : 'https://gogoplay.io'
        
}

def get_m3u8_quality(link):
    
    links = []
    qualities = []
    
    partial_link = link[:link.rfind('/')+1]
    
    r=requests.get(link,headers=headers)
    
    
    for i in start_regex.finditer(r.text):
        res_line,l = i.groups()
        
        #construct the quality 
        qualities.append(str(res_regex.search(res_line).group(1))+"p")
        
        #construct link
        links.append(partial_link+l.strip())
    
    return qualities,links

    