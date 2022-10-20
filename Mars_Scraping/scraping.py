# Import all dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere_scrape(browser)
    
    }

    # stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    
    # visit url
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:
        
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    
    # add try/except for error handling
    try:
        
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_scrape(browser):
    # visit marshemispheres url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # create a list to hold the images and titles
    hemisphere_image_urls = []

    # parse the html with beautifulsoup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # get the links for each of the hemispheres
    hemi_links = hemi_soup.find_all('h3')

    # loop through each hemisphere
    for hemi in hemi_links[0:4]:
        
        # navigate and click the link of the hemisphere
        img_page = browser.find_by_text(hemi.text)
        print(img_page)
        img_page.click()
        html= browser.html
        img_soup = soup(html, 'html.parser')
        
        # scrape the image link
        img_url = 'https://marshemispheres.com/' + str(img_soup.find('img', class_='wide-image')['src'])
        
        # scrape the title
        title = img_soup.find('h2', class_='title').text
        
        # define and append to the dictionary
        hemi_dict = {'img_url': img_url,'title': title}
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

    # print the list that holds the dictionary of each image url and title
    return hemisphere_image_urls

# print and end
if __name__ == "__main__":

    # if running as script, print scraped data
    print(scrape_all())