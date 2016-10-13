# -*- coding: utf-8 -*-
import time
#ここからスクレイピング分
import scrapelib
import json
from bs4 import BeautifulSoup
# seleniumのwebdriverを使う
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys

# Firefoxで動かす用２つ
# from selenium.webdriver import Firefox
# driver = webdriver.Firefox()

driver = webdriver.PhantomJS() # PhantomJSを使う 
driver.set_window_size(1124, 850) # PhantomJSのサイズを指定する

URL = "http://www.slideshare.net/search/slideshow?lang=%2A%2A&page=1&q=Python&qid=38824538-a7bb-43ee-85e5-057d3c1630fc&searchfrom=header&sort=relevance"
driver.get(URL) # slideshareのURLにアクセスする
data_list = []
driver.find_element_by_xpath("//select[@id='slideshows_lang']/option[text()='Japanese']").click()
time.sleep(3) 
for i in range(1,3):
    print(str(i) + u"ページ目")
    data = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(data,"lxml") 
    slide_list = soup.find_all("div",class_="thumbnail-content")
    for slide in slide_list:
        slide_in = {}
        name = slide.find("div",class_="author").text
        
        slide_in["name"] = name.strip()
        
        title = slide.find("a",class_="title title-link antialiased j-slideshow-title").get("title")
        slide_in["title"] = title

        link = slide.find("a",class_="title title-link antialiased j-slideshow-title").get("href")
        slide_in["link"] = "http://www.slideshare.net" + link
        
        imagetag = slide.find("a",class_="link-bg-img").get("style")
        image = imagetag[imagetag.find("url(")+4:imagetag.find(");")]
        slide_in["image"] = image
        
        info = slide.find("div",class_="small-info").string
        slides = info[7:info.find("slides")]
        slide_in["slides"] = slides.strip()
        if "likes" in info:
            likes = info[info.find(", ")+2:info.find("likes")]
        else:
            likes = "0"
        slide_in["likes"] = likes.strip()

        data_list.append(slide_in)
    # Firefoxで動かすためにスクロールさせる
    # driver.execute_script('window.scrollTo(0, 5400)')
    
    # nextarrow = driver.find_elements_by_class_name("arrow") # 次ページへのnextボタンを取得
    # next = nextarrow[1].find_element_by_tag_name("a")
    next = driver.find_element_by_xpath("//li[@class='arrow']/a[@rel='next']")
    next.click()
    time.sleep(3) 
driver.close()
jsonstring = json.dumps(data_list,ensure_ascii=False,indent=2)
print(jsonstring)