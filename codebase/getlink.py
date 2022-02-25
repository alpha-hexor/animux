import requests
from bs4 import BeautifulSoup
import json
import base64
from Cryptodome.Cipher import AES
import yarl


#some global things
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
main_url = "https://www1.gogoanime.pe/"

def get_embade_link(name,ep_num):
    '''
    function to get embade url
    '''
    
    link = main_url + name +"-episode-"+ep_num
    
    try:
        r=requests.get(link,headers=headers)
    except:
        '''
        if sreies starts with ep 0
        '''
        link = main_url+name+"-episode-0"
        r=requests.get(link,headers=headers)
        
    src = r.content
    soup = BeautifulSoup(src,'lxml')

    for item in soup.find_all('a', attrs={'href':'#',"rel":"100",'data-video' : True}):
        url = str(item['data-video'])
    url = "https:" + url
    return url


def pad(data):
    '''
    helper function
    '''
    length = 16 - (len(data) % 16)
    return data + chr(length)*length

def generate_links(url):
    '''
    function to generate streaminhg urls and get qualities
    '''
    qualities = []
    links = []

    s = b"257465385929383"b"96764662879833288"
    p_url = yarl.URL(url)
    ajax_url = "https://{}/encrypt-ajax.php".format(p_url.host)
    encrypted_ajax = base64.b64encode(AES.new(s, AES.MODE_CBC, iv=b'4206913378008135').encrypt(pad(p_url.query.get('id').replace('%3D', '=')).encode()))

    #send the request
    r =requests.get(
        ajax_url,
        params={
            'id': encrypted_ajax.decode(),
            'time': '69420691337800813569'
        },
        headers={'x-requested-with': 'XMLHttpRequest'}
    )

    j = json.loads(r.text)

    #maximum 4 links
    for i in range(4):
        try:
            link = j['source'][i]['file']
            links.append(link)
            q = j['source'][i]['label']
            qualities.append(q)
        except:
            pass


    return qualities, links