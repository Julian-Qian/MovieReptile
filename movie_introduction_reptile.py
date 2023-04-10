# 工具类
import requests
from bs4 import BeautifulSoup
from csv_util import writeToCsvFile
import reptile_configuration
import time


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

def getFileDescription(url,month,picText):
    print(url)
    # 解析具体每个电影的页面获取其海报
    # 爬取完图片后睡眠5s
    html = getFilmHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('div', {"class": "plot"})
    # print(div)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        des=div[0].contents[1].text

        # 将评论写入csv文件
        writeToCsvFile(reptile_configuration.save_description_csv_path,picText,des)
    except:
        print("出现异常！")

    time.sleep(5)

def getTheFilm(filmURL):
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
            getFileDescription(url,count,pic.text)
            countInMounth+=1
        count+=1
    print("下载数据完成！")

if __name__ == '__main__':
    # 生成爬取年份
    year_list=["2019","2020","2021","2022"]

    for y in year_list:
        filmURL= reptile_configuration.China_movie_reptile_website + str(y)
        getTheFilm(filmURL)