#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests as req
import time
from selenium import webdriver



def init_browser():
    executable_path = {"executable_path":"C:\\Windows\chromedriver"}
    return Browser("chrome", **executable_path, headless = False)


def scrape():
    browser = init_browser()
    mars_dictionary = {}
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)

    html = browser.html
    soup = bs(html, "html.parser")
    headline = soup.find('div', class_='list_text').find(class_='content_title').text
    teaser = soup.find_all('div', class_='article_teaser_body')[0].text

    nasa_featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_featured)

    html_featured = browser.html
    soup = bs(html_featured, "html.parser")
    jpl = "https://www.jpl.nasa.gov"

    feat_img = soup.find_all('img')[3]["src"]
    featured_image = jpl + feat_img
 

    mars_facts = "https://space-facts.com/mars/"
    facts_table = pd.read_html(mars_facts)
    fact_df = facts_table[0]
    fact_df.columns = ["Fact Name", "Fact Value"]

    scraped_facts = fact_df.to_html()
    scraped_facts.replace('\n', '')



    usgs = 'https://astrogeology.usgs.gov'
    hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    browser.visit(hemispheres)

    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')


    mars_hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for image in mars_hemispheres:
        
        hemisphere = image.find('h3').text
        hemisphere_url = image.find('a', class_='itemLink product-item')['href']
        
        browser.visit (usgs + hemisphere_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        
        main_image = usgs + soup.find('img', class_='wide-image')['src']
       
        
    
        hemisphere_image_urls.append({"hemisphere" :hemisphere, "main_image": main_image})
        
    mars_dictionary = {
        "headline": headline,
        "teaser": teaser,
        "featured_image": featured_image,
        "mars_facts": scraped_facts,
        "hemisphere_images": hemisphere_image_urls
        }
    return mars_dictionary

    browser.quit()


