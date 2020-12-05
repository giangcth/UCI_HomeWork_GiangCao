from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import cssutils
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars_collection = {}


     # MARS NEWS URL
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    # loop over results to get article titles and bodies:
    result = soup1.find("div", class_="list_text")

    # scrape the article title & body: 
    mars_collection["news_date"] = result.find("div", class_="list_date").text
    mars_collection["news_title"] = result.find("div", class_="content_title").text
    mars_collection["news_body"] = result.find("div", class_="article_teaser_body").text

        
    # MARS FEATURE IMAGE
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html = browser.html
    soup2 = BeautifulSoup(html, 'lxml')

    # Loop over to get the full size of Mars' feature image
    article = soup2.find('article', class_='carousel_item')

    html = f'{article}'
    soup3 = BeautifulSoup(html)
    div_style = soup3.find('article')['style']
    style = cssutils.parseStyle(div_style)
    url = style['background-image']
    url = url.replace('url(', '').replace(')', '')

    mars_collection["featured_image_url"] = "https://jpl.nasa.gov" + url


    # MARS FACTS
    url3 = 'https://space-facts.com/mars/#content/tablepress-comp-mars'
    table = pd.read_html(url3)[0]
    table.columns = ["Facts","Values"]
    clean_table = table.set_index(["Facts"])
    mars_table = clean_table.to_html()
    mars_table = mars_table.replace("\n", "")
    
    mars_collection["facts_table"] = mars_table

    # MARS HEMISPHERES
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)

    hemisphere_image_urls = []
    for runtime in range(4):
        image = browser.find_by_tag('h3')
        image[runtime].click()
        time.sleep(2)
        html = browser.html
        soup4 = BeautifulSoup(html, 'html.parser')

        src = soup4.find('img', class_='wide-image')["src"]
        image_title = soup4.find('h2', class_='title').text
        
        image_url = ['https://astrogeology.usgs.gov' + src]

        dictionary = {"title": image_title, "img_url": image_url}
        
        hemisphere_image_urls.append(dictionary)
        
        browser.back()

    # Collection of information
    mars_collection["hemisphere_image"] = hemisphere_image_urls
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_collection
