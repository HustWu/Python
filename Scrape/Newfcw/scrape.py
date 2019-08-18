import requests
from bs4 import BeautifulSoup
import json
import time

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        print(json.dumps(content,ensure_ascii=False))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def parse_one_page(html):
    # pattern = re.compile(
    #     '<a target="_blank".*?href="(.*?)".*?title="(.*?)">.*?<div.*?class="thumb lazy-load" src="(.*?)".*?">',
    #     re.S
    # )
    soup = BeautifulSoup(html,'lxml')
    items = soup.find_all(name='a')
    #print(items)
    for item in items:
        if(item.has_attr('target') and item.has_attr('title')):
            #print(item['target'],item['title'])
            if(item['target'] == '_blank'):
                #print(item)
                url = 'https://newfcw5.com' + item['href']
                title = item['title']
                secondNode = item.find(class_='thumb lazy-load')
                image = secondNode['data-original']
                #print(secondNode)
                yield {
                    'url': url,
                    'title': title,
                    'image': image
                }

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.6 (KHTML, like Geko) Chorme/52.0.2743.116 Safari/537.6'
    }
    response = requests.get(url,headers = headers)
    if response.status_code == 200:
        return response.text
    return None

if __name__ == '__main__':
    html = get_one_page("https://newfcw5.com/")
    for item in parse_one_page(html):
        write_to_file(item)
    for i in range(100):
        url = ""
        if i == 0:
            continue
        else:
            url = "https://newfcw5.com/" + "latest-updates/" + str(i) + "/"
        html = get_one_page(url)
        for item in parse_one_page(html):
            write_to_file(item)
        time.sleep(1)