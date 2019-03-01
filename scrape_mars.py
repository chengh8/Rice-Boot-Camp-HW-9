from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def scrape():
 #   browser = init_browser()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit the article site
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    #parse the html
    html_article = browser.html
    soup_article = BeautifulSoup(html_article, 'html.parser')

    #pull the title and body
    results_title = soup_article.find_all('div', class_='content_title')
    news_title = results_title[0].text

    results_body = soup_article.find_all('div', class_='article_teaser_body')
    news_p = results_body[0].text

    #visit the twitter on Mars weather
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html_weather = browser.html
    soup_weather = BeautifulSoup(html_weather, 'html.parser')

    #parse the html
    results_weather = soup_weather.find_all('div', class_='js-tweet-text-container')
    weather = results_weather[0].text
    weather = weather.rstrip()
    mars_weather = weather.replace("\n",", ")

    #Use pandas to pull the table for facts about mars
    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['Facts', 'Values']

    #get the Featured image
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)
    browser.click_link_by_partial_text('FULL IMAGE')
    html_picture = browser.html
    soup = BeautifulSoup(html_picture, "html.parser")
    result = soup.find_all("article")
    img_link = result[0].a["data-fancybox-href"]
    featured_img_url = 'https://www.jpl.nasa.gov'+img_link

    #get the hemisphere titles and urls
    url_img = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_img)
    html_picture = browser.html
    soup = BeautifulSoup(html_picture, "html.parser")
    list_Hem = soup.find_all('h3')
    list_dict = []
    
    for i in range(0,len(list_Hem)):
        url_img = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url_img)
        Click = list_Hem[i].text
        browser.click_link_by_partial_text(Click)
        html_picture = browser.html
        soup = BeautifulSoup(html_picture, "html.parser")
        img = soup.find("img",class_='wide-image')["src"]
        img_url = 'https://astrogeology.usgs.gov' + img
        dict = {"title":list_Hem[i].text,
                "img_url":img_url
                }
        list_dict.append(dict)

    #Put all the scraped data into a dictionary
    mars_data = {'article_title':news_title,
                'article_body':news_p,
                'Mars_weather':mars_weather,
                # 'Mars_facts':df,
                'Featured_img':featured_img_url,
                'Mars_hem':list_dict
                }
     
    # Close the browser after scraping
    browser.quit()

    return mars_data