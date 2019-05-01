import requests
from bs4 import BeautifulSoup
import time
import os
import chardet

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    'Host':"movie.douban.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def search(name):
    url='https://movie.douban.com/subject_search?search_text=%s&cat=1002'%name
    html=requests.get(url,headers=headers).text
    item=BeautifulSoup(html).find('div',{'class':'article'}).find('tr',{'class':'item'})
    url=item.find('a').get('href')
    return url
    
def movie_infor(url):
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html).find('div',id='content')
    title=soup.find('h1').get_text().replace('\n','').replace('主演:','')
    table=soup.find('div',id='info')
    try:
        actor=table.find('span',{'class':'actor'}).get_text().replace('\n','')
    except:
        actor='-'
    infors=str(table).split('<br/>')
    date='-'
    runtime='-'
    movie_types=[]
    for item in infors:
        if '上映日期:' in item:
            date=BeautifulSoup(item).get_text().replace('上映日期:','').replace('\n','')
        if '片长:' in item:
            runtime=BeautifulSoup(item).get_text().replace('片长:','').replace('\n','')
        if '类型:' in item:
            movie_types=BeautifulSoup(item).get_text().replace('类型:','').replace('\n','').replace(' ','').split('/')
    try:
        des=soup.find('div',id='link-report').get_text().replace(' ','').replace('\n','')
    except:
        des='-'
    try:
        rate=soup.find('strong',{'class':['ll','rating_num']}).get_text()
    except:
        rate='-'
    try:
        rating_betterthan=soup.find('div',id='interest_sectl').find('div',{'class':'rating_betterthan'}).find_all('a')
    except:
        rating_betterthan=[]
    line=''
    for mtype in movie_types:
        line+='/'+mtype
        for a in rating_betterthan:
            if mtype in str(a):
                try:
                    num=int(a.get_text().split('%')[0])
                    num=str(num/10)
                except:
                    num=''
                line+=' '+num
    line=line[1:]
    template='(\r\n`%s`,\r\n`%s`,\r\n`%s`,\r\n`%s`,\r\n`%s`,\r\n`%s`,\r\n`%s`\r\n),\r\n'
    text=template%(title,des,actor,runtime,rate,date,line)
    return text

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)['encoding']
    if coding=='GB2312':
        coding='GBK'
    return coding

def load_names():
    names=[]
    encoding=get_chardet('movie_name.txt')
    for line in open('movie_name.txt','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','')
        names.append(line)
    return names

def main():
    names=load_names()
    for name in names:
        try:
            url=search(name)
        except:
            print(name,'failed')
            continue
        try:
            text=movie_infor(url)
        except:
            print(name,'failed')
            continue
        f=open('data.txt','a',encoding='utf-8')
        f.write(text)
        f.close()
        print(name,'ok')
        time.sleep(2)

main()