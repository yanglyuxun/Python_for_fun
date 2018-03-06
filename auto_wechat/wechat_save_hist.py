#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open wechat and record the history
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
import time

option = Options()
#option.add_argument("--disable-notifications")
# allow notifications:
prefs={"profile.default_content_settings.popups": 0,
       "profile.default_content_setting_values.notifications": 1}
option.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=option)
driver.get("https://web.wechat.com/")
print('Please log in...')
while True: # setect if you logged in
    try:
        xpath = '//*[@id="J_NavChatScrollBody"]/div/div[2]/div'
        user = driver.find_element_by_xpath(xpath)
        break
    except:
        time.sleep(1)
print('You have logged in. Please wait.')
time.sleep(2)


#def get_messages(sender='you'):
#    '''sender in ['you','me']'''
#    mesele = driver.find_elements_by_class_name(sender)
#    mesele = [m0.find_element_by_class_name('bubble_cont') for m0 in mesele]
#    return [i.text for i in mesele]

def get_username():
    uname = driver.find_element_by_class_name('title_name')
    return uname.text

def get_messages():
    msgs = driver.find_elements_by_class_name('message')
    out = []
    for m in msgs:
        for e in m.find_elements_by_class_name('message_system'):
            out.append(['sys',e.text])
        for e in m.find_elements_by_class_name('content'):
            for e2 in e.find_elements_by_class_name('bubble'):
                out.append([e2.get_attribute('class').split()[-1],e.text])
        #print(m.get_attribute('class'))
        #print(m.get_attribute('outerHTML'))
        #print(m.text)
    return out

def check_active():
    try:
        xpath = '//*[@id="J_NavChatScrollBody"]/div/div[2]/div'
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


#mm = driver.find_elements_by_xpath("//div[@class='clearfix']")
#[m.text for m in mm]
#m=mm[0]
#html = m.get_attribute('outerHTML')
#html1 = html.split('\n')
#html1 = [h.strip() for h in html1]
#[h for h in html1 if h.startswith('<!--')]
        
    
class history_writer(object):
    def __init__(self, dir='history/'):
        self.hist = {}
        self.dir = dir
############ continue here
        
        
his = history_writer()
while True:
    if not check_active():
        exit
    username = get_username()
    if username in his:
        his[username] = combine(his[username],get_messages())
    else:
        his[username] = get_messages()
    
    time.sleep(1)
