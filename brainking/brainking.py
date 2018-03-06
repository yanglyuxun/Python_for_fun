#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 16:44:08 2018

@author: ylx
"""

import pexpect
import json,time,subprocess
from numpy import random

def shell(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE,shell=True)
    return result.stdout.decode()

def process(l):
    ''' process the output of the program'''
    if l.find('server will at port:8998')>=0:
        print('port:8998')
    elif l.find('WARN:')>=0:
        print('WARN')
    elif l.find('Cost time')>=0:
        print(' '.join(l.split(' ')[2:]))
    elif l.find('response findQuiz')>=0:
        q = l.split('response findQuiz')[1]
        show_quiz(q)
    elif l.find('Response findQuiz')>=0:
        q = l.split('Response findQuiz')[1]
        show_quiz(q)
    elif l.find('response choose')>=0:
        s = ' '.join(l.split(' ')[6:])
        show_result(s)
    elif l.find('Saving')>=0:
        print('Right answer: ',l.split(',')[1].strip())
    else:
        print(l)

def show_quiz(q):
    ''' show the quiz and get the answer'''
    quiz = json.loads(q)['data']
    question = quiz['quiz']
    print('Q:',question)
    choices = []
    scores = []
    for i,c in enumerate(quiz['options']):
        depart = c.replace(']','').split('[')
        if len(depart)==1:
            choices.append(depart[0])
            scores.append(0)
        elif len(depart)==2:
            choices.append(depart[0])
            if depart[1]=='标准答案':
                scores.append(99999)
            else:
                scores.append(int(depart[1]))
        else:
            print('ERROR: ', quiz['options'])
            return
    if ('不' in question) and (99999 not in scores):
        best = min(scores)
    else:
        best = max(scores)
    for i in range(4):
        if scores[i]==99999:
            print("%i.  %s    [%s]"%(i+1,choices[i],'标准答案!!!!!!'))
            answer = i
        elif scores[i]==best:
            print("%i.  %s    [%i] ****"%(i+1,choices[i],scores[i]))
            answer = i
        else:
            if scores[i]>0:
                print("%i.  %s    [%i]"%(i+1,choices[i],scores[i]))
            else:
                print("%i.  %s"%(i+1,choices[i]))
    touch_answer(answer)
    

def touch_answer(an):
    ''' use adb to touch the answer'''
    x,y = {0:(540,900), 1:(540,1090), 2:(540,1280), 3:(540,1480)}[an]
    t0 = time.time()
    time.sleep(2.5)
    print('AUTO tap:',an+1,' ... ')
    while time.time()-t0<7:
        x0 = x + random.randint(-100,100)
        y0 = y + random.randint(-40,40)
        shell('adb shell input tap %i %i'%(x0,y0))
    print('AUTO tap: Done.')

def touch_continus():
    x,y=540,1280
    x0 = x + random.randint(-100,100)
    y0 = y + random.randint(-10,10)
    shell('adb shell input tap %i %i'%(x0,y0))
    time.sleep(1)
    x,y=540,1700
    x0 = x + random.randint(-100,100)
    y0 = y + random.randint(-10,10)
    shell('adb shell input tap %i %i'%(x0,y0))
    time.sleep(7)

def show_result(s):
    ''' show the result of the choice'''
    result = json.loads(s)['data']
    if result['yes']:
        print('Correct!')
    else:
        print('Wrong!')

with pexpect.spawn('./brain', timeout=None) as p:
    while True:
        try:
            p.expect('\n',timeout = 13)
            process(p.before.decode())
        except:
            print('Restarting the game...')
            touch_continus()
        
