# Import Splinter, BeautifulSoup, pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

#define scrape_all and initiate browser
def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    return data

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

# Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    #begin scrape
    slide_elem.find("div", class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p

    return news_title, news_p

#### Featured Images

def featured_image(browser):

    # Visit URL for images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    return df.to_html()

def mars_hemispheres(browser):
    # Visit the Astrogeology USGS site:
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create empty list to hold hemisphere url's & titles:
    hemisphere_list = []

    #get the full size images
    browser.is_element_present_by_css("thumb", wait_time=2)
    thumbnails = browser.find_by_tag('h3')

    #Create 4 hemisphere pics/titles
    for i in range(0,4):
        
        #Click on the thumbnail for each image
        thumbnails[i].click()

        #Parse
        html = browser.html
        hemisphere_soup = BeautifulSoup(html, 'html.parser')

        #Find the relative image url
        img_url_rel = hemisphere_soup.select_one('.wide-image').get('src')
        hemisphere_title = hemisphere_soup.find('h2', class_='title').get_text()
        img_url = f'https://astrogeology.usgs.gov{img_url_rel}'

        #Add to hemishphere_list dictionary
        hemisphere_dictionary = {}
        hemisphere_dictionary['img_url'] = img_url
        hemisphere_dictionary['title'] = hemisphere_title 
        hemisphere_list.append(hemisphere_dictionary)

        #Hit the back button on the browser
        browser.back()

        #iterate through all 4 
        browser.is_element_present_by_css("thumb", wait_time=2)
        thumbnails = browser.find_by_tag('h3')

    # Return the completed list with pics/titles
    return hemisphere_list

browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


