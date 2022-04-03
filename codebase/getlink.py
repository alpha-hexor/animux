import requests
from bs4 import BeautifulSoup
import json
import base64
from Cryptodome.Cipher import AES
import yarl

#huge help from animedl

#some global things
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
main_url = "https://gogoanime.fi/"

s=b"63976882873559819639988080820907"
iv= b"4770478969418267"

#pad_data="\x08\x0e\x03\x08\t\x03\x04\t"

def get_embade_link(name,ep_num):
    '''
    function to get emabde url
    '''
    link = main_url + name +"-episode-"+ep_num
    try:

        r=requests.get(link,headers=headers)
    except:
        link = main_url+name+"-episode-0"
        r=requests.get(link,headers=headers)
    
    src = r.content
    soup = BeautifulSoup(src,'lxml')

    for item in soup.find_all('a', attrs={'href':'#',"rel":"100",'data-video' : True}):
        url = str(item['data-video'])
    url = "https:" + url
    return url

# def get_crypto(url):
#     '''
#     function to get crypto data
#     '''
#     r=requests.get(url,headers=headers)
#     src = r.content
#     soup = BeautifulSoup(src,'lxml')
#     for item in soup.find_all('script',attrs={'data-name':'crypto','data-value':True}):
#         crypto = str(item['data-value'])
#     return crypto
    
def pad(data):
    '''
    helper function
    '''
    return data + chr(len(data) % 16) * (16 - len(data) % 16)


def decrypt(data):
    '''
    function to decrypt data
    '''
    return AES.new(s, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))

def generate_links(url):
    '''
    function to generate streaminhg urls and get qualities
    '''
    qualities = []
    links = []

    # crypto_data=get_crypto(url)
    # #get the decrypted crypto value
    # decrypted_crypto = decrypt(crypto_data)
    # new_id = decrypted_crypto[:decrypted_crypto.index(b"&")].decode()
    
    
    p_url = yarl.URL(url)
    ajax_url = "https://{}/encrypt-ajax.php".format(p_url.host)
    encrypted_ajax = base64.b64encode(
        AES.new(s,AES.MODE_CBC,iv=iv).encrypt(
            pad(p_url.query.get('id')).encode()
        )
    )

    #send the request
    r =requests.get(
        ajax_url,
        params={
            'id': encrypted_ajax.decode(),
            
        },
        headers={'x-requested-with': 'XMLHttpRequest'}
    )

    j = json.loads(
        decrypt(r.json().get("data")).strip(
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"
        )
    )
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
