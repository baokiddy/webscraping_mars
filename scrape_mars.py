# Import Splinter and Beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Create mars_data dict that we can insert into mongo
    mars_data = {}

    # NASA Mars News
    # Visit the NASA URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Scrape the website and collect the latest News Title and Paragraph Text.
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_title = soup.find('div', class_='content_title').get_text()
    latest_paragraph = mars_weather = browser.find_by_css(f'div[class="article_teaser_body"]').first.text

    mars_data['nasa_article_title'] = latest_title
    mars_data['nasa_article_content'] = latest_paragraph

    ######################################################################################################

    # JPL Mars Space Images - Featured Image
    # Visit the JPL URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Design an XPATH selector to grab the feature image
    xpath = '//footer//a[@class="button fancybox"]'

    # Use splinter to Click the featured image and bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    featured_image_url = browser.find_by_css(f'img[class="fancybox-image"]').first["src"]

    mars_data['jpl_mars_feature_url'] = featured_image_url

    ####################################################################################################

    # Mars Weather
    # Visit the Mars Weather twitter URL
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape the website and collect the Mars weather forecast from the latest tweet.
    mars_weather = browser.find_by_css(f'div[class="js-tweet-text-container"]').first.text

    mars_data['latest_mars_weather'] = mars_weather

    #####################################################################################################

    # Mars Facts
    # Visit the Space facts URL
    url = "http://space-facts.com/mars/"
    browser.visit(url)

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    import pandas as pd

    table = pd.read_html(url)
    table

    df = table[0]
    df.head()

    # Use Pandas to convert the data to a HTML table string
    html_table = df.to_html()

    mars_data['mars_facts'] = html_table

    ######################################################################################################

    # Mars Hemispheres
    # Visit the Space facts URL
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Import time library for timed delay
    import time

    # Design an XPATH selector to grab full res image and title
    xpath = '//section//img[@class="thumb"]'

    # Use splinter to Click the image and bring up the correct webpage
    results = browser.find_by_xpath(xpath)

    img_url =[]
    title = []
    hemisphere = {}
    hemisphere_image_urls = []

    # Iterate through webpages to collect the full res image and page title
    for i in range(len(results)):
        results[i].click()
        
        img = browser.find_by_css(f'img[class="wide-image"]')['src']
        img_title = browser.find_by_css(f'h2[class="title"]').first.text   
        
        hemisphere["title"] = img_title
        hemisphere["img_url"] = img
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()
        time.sleep(5)
        
        xpath = '//section//img[@class="thumb"]'
        results = browser.find_by_xpath(xpath)
        hemisphere = {}
        
    mars_data['mars_hemisphere_images'] = hemisphere_image_urls

    browser.quit()
    return mars_data

