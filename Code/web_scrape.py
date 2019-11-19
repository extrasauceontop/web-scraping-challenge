# Import dependencies
import requests
import urllib
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import time
import pandas as pd

def scrape():
    # Create Browser instance
    executable_path = {"executable_path":"chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Navigate to Nasa Mars website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Time for Java to load articles
    time.sleep(1)

    # Set up soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # Grab first title and paragraph
    first_grid = soup.find(attrs={'class': 'list_text'})
    title = first_grid.find(attrs={'target': '_self'}).text.strip()
    paragraph = first_grid.find(attrs={'class': 'article_teaser_body'}).text.strip()

    # Navigate to Mars Weather Twitter
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Set up soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the latest tweet text
    tweet_text = soup.find(attrs={'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text.strip()

    # Read tables from Mars facts website
    dfs = pd.read_html("https://space-facts.com/mars/")

    # Get the table about mars
    df = dfs[0]
    df = df.rename(columns={0: 'Attributes', 1: 'Facts'})
    df = df.to_csv("data.csv", index=False)
    
    # Navigate to Hemisphere images site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_short = 'https://astrogeology.usgs.gov/'
    browser.visit(url)

    # Set up soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # Get image source tags
    images = soup.find_all(attrs={'class': 'thumb'})
    sources = []
    for image in images:
        source = image['src']
        source = url_short + source
        sources.append(source)

    # Store image URLs
    image_urls = {'Valles Marineris Hemisphere': sources[0],
                    'Cerberus Hemisphere': sources[1],
                    'Schiaparelli Hemisphere': sources[2],
                    'Syrtis Major Hemisphere': sources[3]}

    final_output = {'news_title': title, 'news_paragraph': paragraph, 'latest_tweet': tweet_text, 'images': image_urls}

    browser.quit()

    return(final_output)