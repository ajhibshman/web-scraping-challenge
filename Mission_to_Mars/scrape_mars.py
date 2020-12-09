from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pprint import pprint
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape_info():
    browser = init_browser()
    mars = {}

    # get latestnews title and paragraph, save to variables
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles=soup.find_all(name='li', class_='slide')
    mars["news_title"]=articles[0].find('div',class_='content_title').text
    mars["news_p"]=articles[0].find('div',class_='article_teaser_body').text

    #scrape 2- JPL Mars Space Images 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image=soup.find('img', class_='fancybox-image')
    featured_image_url=image.get('src')
    mars['image1']='https://www.jpl.nasa.gov' + featured_image_url
    

    #scrape 3- Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tables=pd.read_html(url)
    df=tables[0]
    df1=df.set_index(0)
    df1=df1.rename(columns={0: '',1:'Mars' })
    df1.index.name=None
    df1.head()
    print("helooooo!!!")
    html_table = df1.to_html()
    html_table.replace('\n', '')
    mars["table1"]=html_table
    
    # #obtain high resolution images for each of Mar's hemispheres.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemispheres=[]

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results=soup.find_all(name='div', class_='item')
    for result in results:
        title=result.find('h3').text
    
        browser.links.find_by_partial_text(title).click()
        html2=browser.html
        soup2=BeautifulSoup(html2,'html.parser')
        images=soup2.find(name='div',class_='downloads')
        hem_url=images.a['href']
    
        browser.back()
        hemispheres.append({"title": title, "img_url": hem_url})
    
    pprint(hemispheres)
    mars["hemispheres_list"]=hemispheres

    browser.quit()

    #return results
    return mars

   

    
