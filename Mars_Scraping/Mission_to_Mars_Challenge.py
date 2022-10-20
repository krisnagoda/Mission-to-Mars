# import splinter and beautifulsoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set the executable path and initialize splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Title and Summary 

# visit the nasa mars news site

url = 'https://redplanetscience.com/'
browser.visit(url)

# set delay for loading the page

browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the html parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# use the parent element to find the first `a` tag and save it as `news_title`

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# visit jpl url

url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse the resulting html with soup

html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# use the base url to create an absolute URL

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# scrape the entire table with pandas' .read_html() function

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

# ### Visit the NASA Mars News Site

# visit redplanetscience url

url = 'https://redplanetscience.com/'
browser.visit(url)

# delay for page load time

browser.is_element_present_by_css('div.list_text', wait_time=1)

# convert the browser html to a soup object

html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

# visit spaceimages-mars url

url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parse the resulting html with bs

html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# use the base url to create an absolute url

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# ### D1: High-Res Mars’ Hemisphere Images and Titles

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

for hemi in hemi_links:
    
    # navigate and click the link of the hemisphere
    
    img_page = browser.find_by_text(hemi.text)
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

hemisphere_image_urls

# end the automated browsing session

browser.quit()





