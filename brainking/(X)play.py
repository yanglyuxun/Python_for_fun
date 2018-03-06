#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android API by uiautomator with abd tools
"""

import subprocess
#from keras.preprocessing import image
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle
import time
import pytesseract as pyt
import webbrowser
import requests
#from uiautomator import device as d

def shell(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE,shell=True)
    return result.stdout.decode()

def screen_shot():
    t=shell("adb shell screencap -p > tmp.png")
    if t: print(t)
    return Image.open('tmp.png')

def get_question(img):
    question = np.array(img.crop((0,500,1080,810)).convert('L'))
    question = cv2.threshold(question,230,255,cv2.THRESH_BINARY_INV)[1]
    question = Image.fromarray(question)
    return pyt.image_to_string(question, lang='chi_sim')

def get_choices(img):
    chs = img.crop((230,830,850,1550))
    choices = []
    choices.append(chs.crop((0,0,620,135)))
    choices.append(chs.crop((0,190,620,330)))
    choices.append(chs.crop((0,380,620,520)))
    choices.append(chs.crop((0,575,620,710)))
    return [pyt.image_to_string(t.convert('L'), lang='chi_sim') for t in choices]
    

def open_wabpage(question):  
    webbrowser.open('https://baidu.com/s?wd=' + question)  

def words_count(question,answers):  
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})  
    body = req.text  
    counts = []  
    for answer in answers:  
        num = body.count(answer)  
        counts.append(num)  
        print(answer + " ---> " + str(num))
    return counts;  

def search_count(question,answers):  
    counts = []  
    for answer in answers:  
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question +"%20"+answer})  
        body = req.text  
        start = body.find(u'About ') +5
        body = body[start:]  
        end = body.find(u"results")  
        num = body[:end]  
        num = num.replace(',', '')  
        counts.append(int(num))  
        print(answer + " ---> " + str(num))
    return counts 

if __name__=='__main__':
    while input()!='q':
        img=screen_shot()
        question = get_question(img).replace(' ','')
        answers = get_choices(img)
        #open_wabpage(question)
        print('max=',answers[np.argmax(words_count(question,answers))])
        print('max=',answers[np.argmax(search_count(question,answers))])
