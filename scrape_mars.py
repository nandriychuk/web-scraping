from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # # MARS NEWS
    # Visit NASA Web site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    
    #MARS IMAGE
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")

    article = soup.find('article', class_="carousel_item")
    style_link = article["style"]
    featured_image = style_link.split("('", 1)[1].split("')")[0]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image

    #MARS WEATHER
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")

    mars_weather = soup.find_all('p',class_="TweetTextSize")[1].text
    

    #MARS INFO TABLE
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")

    table = soup.find('table', id="tablepress-mars")
    table_rows = table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()] 
        if row:
            res.append(row)

    mars_df = pd.DataFrame(res)
    mars_df=mars_df.to_html(index=False, col_space=100, header=False, border=1)##.replace('\n', '')   , col_space=50
    mars_df = mars_df.replace('\n', '')
    

    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")

    links = browser.find_by_css('a.product-item h3')

    hemisphere_image_urls = []
    for i in range(len(links)):
        url_dict = {}
        url_dict["title"] = browser.find_by_css('a.product-item h3')[i].text
        browser.find_by_css('a.product-item h3')[i].click()

        url_dict["img_url"] = browser.find_link_by_text("Sample").first["href"]

        hemisphere_image_urls.append(url_dict)
        browser.back()
    
# Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_img": featured_image_url,
        "weater_twitter": mars_weather,
        "mars_facts": mars_df,
        "hemispheres": hemisphere_image_urls,
    }

    browser.quit()

    # Return results
    return mars_data