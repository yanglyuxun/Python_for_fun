#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import webbrowser as wb
#import os

data = pd.read_json('data.json')
done = data['done']
print('%s/%s (%s%%)done.'%(sum(done),len(done),sum(done)/len(done)))
if sum(done)==len(done):
    exit
undone = data[done==False]
new = undone.sample()
print(new.iloc[:,3:])
wb.open(new['url'].iloc[0], new=2, autoraise=False)
if input('Done? (y/n):')=='y':
    data.loc[new.index[0],'done'] = True
    data.to_json('data.json')

