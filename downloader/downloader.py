#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 12:49:48 2018

@author: ylx
"""

url='http://hdeuropix.com/tvseries/doctor-who-online/doctor-who-season-8-hd-with-subtitles-europix'

from selenium import webdriver
import time,json,os
import pandas as pd

#from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# now install Adblock

driver.get(url)
# now open dev tools, select the media tab

links = driver.find_elements_by_name('link')


for i in range(len(links)):
    links[i].click()
    links[i].click()
    xpath='//*[@id="opis"]/div[1]'
    video = driver.find_element_by_xpath(xpath)
    video.click()
    video.click()

# save to 'hdeuropix.com.har'
fname = 'hdeuropix.com.har'
with open(fname) as f:
    har=json.load(f)['log']['entries']

urls = [h['request']['url'] for h in har]


mp4 = [u for u in urls if u.find('mp4')>=0 and u.find('Doctor.Who')>=0]
data = pd.DataFrame(columns=['mp4','vtt'])
for u in mp4:
    name = u.split('/')[-1].split('.')[3]
    data.loc[name,'mp4'] = u
    
print('\n'.join(data['mp4']))

vtt = [u for u in urls if u.find('vtt')>=0]
vtt_new = []
for v in vtt:
    if v not in vtt_new:
        vtt_new.append(v)
data['vtt']=vtt_new

for name in data.index:
    url = data.loc[name,'mp4']
    fname = url.split('/')[-1].split('?')[0].replace('.mp4','.vtt')
    os.system('wget -O %s.vtt %s'%(fname,data.loc[name,'vtt']))