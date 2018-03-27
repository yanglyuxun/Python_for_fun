
# coding: utf-8

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup

# In[15]:

def get(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    response = requests.get(url,headers = headers)
    print('Done.')
    return BeautifulSoup(response.content,'lxml')

# In[16]:

url_base = 'https://www.nowcoder.com/ta/2017test?query=&asc=true&order=&page=%s'
page_range = range(1,5)
urls = [url_base%i for i in page_range]
soups = [get(u) for u in urls]

# In[21]:
preurl = 'https://www.nowcoder.com'
data=[]
for soup in soups:
    d0 = pd.read_html(str(soup),header=0)[0]
    tb = soup.table
    rows = tb.find_all('tr')
    us = []
    for row in rows[1:]:
        cols = row.find_all('td')
        us.append(preurl+row.a.attrs['href'])
    d0['url'] = us
    data.append(d0)
data = pd.concat(data,ignore_index=True)
data['done'] = False
data.to_json('data.json')


