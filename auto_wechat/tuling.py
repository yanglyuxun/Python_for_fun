#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tuling123.com API
Created on Mon Dec 11 18:18:33 2017

"""

#!usr/bin/env python3
# -*- coding:utf-8-*-


import json
import requests

class tulingrobot(object):
    def __init__(self):
        pass
    def get_data(self,text):
        data = {'key':'*',
                'info':text,
                'loc':"*",
                'userid':'XiXi'}
        return data
    def get_answer(self,text):
        data = self.get_data(text)
        url = 'http://www.tuling123.com/openapi/api'
        response = requests.post(url=url, data=json.dumps(data))
        response.encoding = 'utf-8'
        result = response.json()
        answer = result['text']
        return answer
