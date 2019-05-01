import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}

def comments(movieid,fromdate,todate):
    start=0
    rating={}
    comments={}
    while True:
        url='https://m.douban.com/rexxar/api/v2/movie/{}/interests?count=20&order_by=latest&start={}&ck=&for_mobile=1'.format(movieid,start)
        html=requests.get(url,headers=headers).text
        print(movieid,start)
        start+=25
        data=json.loads(html)['interests']
        if len(data)==0:
            break
        for item in data:
            date=item['create_time'].split(' ')[0]
            int_date=int(date.replace('-',''))
            if int_date>todate:
                continue
            if int_date<fromdate:
                continue

            f=open('data.txt','a')
            f.write(str(item)+'\n')
            f.close()
            try:
                value=item['rating']['value']
                try:
                    rating[date].append(value)
                except:
                    rating[date]=[value]
            except:
                pass
            vote_count=item['vote_count']
            if vote_count!=0:
                try:
                    comments[date]+=1
                except:
                    comments[date]=1
    return {'rating':rating,'comments':comments}

def load_movie():
    movies=[]
    for line in open('movies.txt','r'):
        line=line.replace('\n','')
        movies.append(line.split('|'))
    return movies

def main():
    movies=load_movie()
    for movie in movies:
        movieid=movie[-1]
        fromdate=int(movie[1])
        todate=int(movie[2])
        result=comments(movieid,fromdate,todate)
        f=open('result.txt','a')
        f.write(str(result)+'\n')
        f.close()
        print(movie,'ok')

main()
