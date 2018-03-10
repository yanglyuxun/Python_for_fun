#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import webbrowser as wb
import os

data = pd.read_json('data.json')
data = data.sort_values('Acceptance',ascending=False)
if 'Done' not in data: data['Done'] = data['Done_online']

find = False
for i in data.index:
    if not data.loc[i,'Done']:
        if data.loc[i,'artivle_url']:
            wb.open('https://leetcode.com'+data.loc[i,'artivle_url'])
        else:
            wb.open('https://www.google.com/search?q='+str(i)+'. '+data.loc[i,'Title'])
        find = True
        break
if find:
    if not os.path.exists('drafts'): os.mkdir('drafts')
    if not os.path.exists('drafts/%s.sql'%i):
        with open('drafts/%s.sql'%i, 'w') as f:
            f.write('')
    os.system('xed drafts/%s.sql'%i)
    if input('Done? (y/n):')=='y':
        data.loc[i,'Done'] = 'read'
        data.to_json('data.json')
