import requests
from bs4 import BeautifulSoup
from reptile_configuration import save_file_dir_path,save_file_dir_path_2018
import time
import os




def getFilmHTMLText(url,code='utf-8'):
    try:
        #加上头部信息后可避免有时候抓取为空的情况
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        r=requests.get(url,timeout=30,headers=headers)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return ""

def getThePicture(url,month,countInMonth,fileLoadPath,picText):
    print(url)
    #解析具体每个电影的页面获取其海报
    #爬取完图片后睡眠5s
    html=getFilmHTMLText(url)
    soup=BeautifulSoup(html,'html.parser')
    img=soup.find_all('img',{"class":"poster"})
    print(picText)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        r=requests.get(img[0].attrs['src'],timeout=30,headers=headers)
        r.raise_for_status()
        filePath=fileLoadPath+str(month)+'月\\'+str(picText)+'.jpg'
        print(filePath)
        with open(filePath,'wb') as f:
                f.write(r.content)
    except:
        print("出现异常！")

    time.sleep(5)

def getTheFilm(lst,filmURL):
    html=getFilmHTMLText(filmURL)
    soup=BeautifulSoup(html,'html.parser')
    dl=soup.find_all('dl',{"class":"clear"})
    count=1
    for f in dl:
        x=f.find_all('a',{"class":"film"})
        print("月份" + str(count))
        countInMounth=0
        for pic in x:
            #https://www.1905.com
            #get the concrete film's url
            print(type(pic))
            # print(pic.text)
            url="https://www.1905.com"+pic.attrs['href']
            getThePicture(url,count,countInMounth,save_file_dir_path_2018,pic.text)
            countInMounth+=1
        count+=1
    print("下载海报完成！")
if __name__ == '__main__':
    filmURL="https://www.1905.com/mdb/film/calendaryear/2018"
    flist=[]
    getTheFilm(flist,filmURL)