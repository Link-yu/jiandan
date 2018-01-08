

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import lxml

Directory = 'E:/meizitu/'
base_url = "http://jandan.net/ooxx/page-"
path = "F:\chrome\chromedriver.exe"
driver = webdriver.PhantomJS(executable_path=r'F:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# driver = webdriver.Chrome(executable_path=path)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
img_url = []
urls = ["http://jandan.net/ooxx/page-{}#comments".format(str(i)) for i in range(400, 500)]
def getMeiziTu(page):
    meizi_url = base_url + str(page) + "#comments"
    respone = requests.get(meizi_url, headers=headers)
    respone.encoding = 'utf-8'
    soup = BeautifulSoup(respone.text, "html5lib")
    if soup.find(text=re.compile('屏蔽')) == None:
        print('=============================')
        print('正在下载第 ' + str(page) + ' 页')
        #               存储包含图片地址的标签
        img = []
        imgall = soup.body('li', id=re.compile("comment-"))
        for tmp in imgall:
            img += tmp.div.find(
                'div', class_='row').find(
                'div', class_='text').find_all(
                'img', src=True)
        for n, girl in enumerate(img):
            print('       第 ' + str(n) + ' 张', end='')
            if not girl.has_attr('org_src'):
                url = girl['src']
                with open(Directory + '妹纸图' + str(page) + '-' + str(n)
                                  + url[-4:], 'wb') as f:
                    f.write(requests.get(url).content)
            else:
                url = girl['org_src']
                with open(Directory + '妹纸图' + str(page) + '-' + str(n)
                                  + url[-4:], 'wb') as f:
                    f.write(requests.get(url).content)
            print('...OK!')
        print('第 ' + str(page) + ' 页下载完成啦！！！')
        return True

def getImg():
    n = 1
    for url in img_url:
        print('第' + str(n) + ' 张', end='')
        with open(Directory + url[-15:], 'wb') as f:
            f.write(requests.get(url).content)
        print('...OK!')
        n = n+1

def getImgUrl(url):
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")  # 解析网页
    images = soup.select("a.view_img_link")  # 定位元素
    for i in images:
        z = i.get('href')
        if str('gif') in str(z):
            pass
        else:
            http_url = "http:" + z
            img_url.append(http_url)
            print(http_url)


if __name__ == "__main__":
    for url in urls:
        getImgUrl(url)
    getImg()
    print("")



