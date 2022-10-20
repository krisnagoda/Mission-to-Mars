#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import splinter and beautifulsoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# set the executable path and initialize splinter

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Title and Summary 

# In[3]:


# visit the nasa mars news site

url = 'https://redplanetscience.com/'
browser.visit(url)

# set delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# set up the html parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# assign the title and summary text to variables

slide_elem.find('div', class_='content_title')


# In[6]:


# use the parent element to find the first `a` tag and save it as `news_title`

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# visit jpl url

url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# parse the resulting html with soup

html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# find the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# use the base url to create an absolute URL

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


# scrape the entire table with pandas' .read_html() function

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ### Visit the NASA Mars News Site

# In[15]:


# visit redplanetscience url

url = 'https://redplanetscience.com/'
browser.visit(url)

# delay for page load time

browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[16]:


# convert the browser html to a soup object

html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[17]:


slide_elem.find('div', class_='content_title')


# In[18]:


# use the parent element to find the paragraph text

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[19]:


# visit spaceimages-mars url

url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[20]:


# find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[21]:


# parse the resulting html with bs

html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[22]:


# find the relative image url

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[23]:


# use the base url to create an absolute url

img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[24]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[25]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[26]:


df.to_html()


# ### D1: High-Res Mars’ Hemisphere Images and Titles

# In[27]:


# visit marshemispheres url

url = 'https://marshemispheres.com/'
browser.visit(url)


# In[30]:


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


# In[31]:


# print the list that holds the dictionary of each image url and title

hemisphere_image_urls


# In[32]:


# end the automated browsing session

browser.quit()


# In[ ]:




