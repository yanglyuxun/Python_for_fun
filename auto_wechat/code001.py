#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
from tuling import tulingrobot

driver = webdriver.Chrome()
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

i=2 # the starting index
friends = {}
while True: 
    try:
        xpath = '//*[@id="J_NavChatScrollBody"]/div/div['+str(i)+']/div'
        user = driver.find_element_by_xpath(xpath)
        nickname = user.find_element_by_class_name('nickname').text
        friends[nickname]=user
        i+=1
    except:
        break
print('All friends found:')
print([i for i in friends.keys()])

# functions
def sendtext(t):
    print('Sent words: "'+t+'"')
    user.click()
    inputbox.send_keys(t)
    inputbox.send_keys('\n')
def print2(t):
    print('\r'+t,end='')
def print3(sec, min):
    print2('Time left: '+str(min)+':'+str(sec)+'     ')
def wait(sec=0,min=0,detect=None):
    total = int(sec+min*60)
    min,sec = divmod(total,60)
    print3(sec,min)
    while sec>0 or min>0:
        time.sleep(1)
        if sec>0:
            sec-=1
        else:
            sec+=59
            min-=1
        print3(sec,min)
        if detect is not None:
            detect()
    print()
    return
def get_messages(sender='you'):
    '''sender in ['you','me']'''
    mesele = driver.find_elements_by_class_name(sender)
    mesele = [m0.find_element_by_class_name('bubble_cont') for m0 in mesele]
    return [i.text for i in mesele]
def detect0():
    user.click()
    xpath= '//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div/pre'
    driver.find_element_by_xpath(xpath)

# choose the user

nickname = 'XiXi'
#nickname = 'File Transfer'

user = friends[nickname]
user.click()
print('Select "'+nickname+'"')
inputbox = driver.find_element_by_xpath('//*[@id="editArea"]')

# the xpath of the message
#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div/pre
#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[3]/div/div/div/div/div/div/div/pre
#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[3]/div/div/div/div[2]/div/div/div/pre

#%% auto send messages
#while True:
#    sendtext('测试')
#    wait(min=5)

#%% test auto reply
mess0 = get_messages()
tl = tulingrobot()
while True:
    try:
        mess1 = get_messages()
    except:
        continue
    if mess0!=mess1 and len(mess1)>0:
        newmess = mess1[-1]
        print('Received: "'+newmess+'"')
        sendtext(tl.get_answer(newmess))
        mess0=mess1
    time.sleep(1)