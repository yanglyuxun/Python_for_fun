#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:48:12 2017

@author: ylx
"""

import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import dropbox
import getpass
import json
import time
import os

class AESCipher(object):
    def __init__(self): 
        self.bs = 32
        self.update_key()
    def check_key(self,enc,target):
        return self.decrypt(enc)==target
    def update_key(self):
        self.key = hashlib.sha256(getpass.getpass('Input the key:').encode()).digest()
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)
    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    def _unpad(self,s):
        return s[:-ord(s[len(s)-1:])]

class Dropbox_tool(object):
    def __init__(self, token):
        self.cipher = AESCipher()
        self.jsonen = json.JSONEncoder()
        self.jsonde = json.JSONDecoder()
        while True:
            try:
                self.dbx = dropbox.Dropbox(self.cipher.decrypt(token))
                break
            except Exception as e: 
                print(e)
                print('The key may be incorrect.')
                self.cipher.update_key()
    def read(self,path):
        try:
            dt = self.dbx.files_download(path)
            return self.cipher.decrypt(dt[1].content)
        except Exception as e: 
            print(e)
            return None
    def write(self,txt,path):
        try:
            self.dbx.files_upload(self.cipher.encrypt(txt),path)
            return True
        except Exception as e: 
            print(e)
            return None
    def json_read(self,path):
        return self.jsonde.decode(self.read(path))
    def json_write(self,obj,path):
        return self.write(self.jsonen.encode(obj),path)
    def ls(self,path=''):
        names = []
        try:
            for entry in self.dbx.files_list_folder(path).entries:
                names.append(entry.name)
            return names
        except Exception as e: 
            print(e)
            return None

class recorder(object):
    def __init__(self,token):
        self.token = token
        self.dbt = Dropbox_tool(token)
        self.fnames = self.dbt.ls()
        if self.fnames is None:
            return None
        if 'list.txt' not in self.fnames:
            self.dbt.json_write({},'/list.txt')
        self.list = self.dbt.json_read('/list.txt')
    def print_list(self):
        self.list = self.dbt.json_read('/list.txt')
        print('The list of all files:')
        if self.list:
            for i in self.list:
                print(i + ': ' + self.list[i][0])
        else:
            print('(None)')
    def write_list(self):
        print('Writing the new list...')
        timename = str(time.time()).replace('.','_')
        self.dbt.dbx.files_move('/list.txt','/list_backup/'+timename)
        self.dbt.json_write(self.list,'/list.txt')
        print('Donw.')
    def show(self,name):
        if name not in self.list:
            print('Name Error.')
            return None
        else:
            cur = self.list[name][2] #current number 
            print(self.dbt.read('/'+self.list[name][1]+'/'+str(cur)))
    def write(self,name):
        if name not in self.list:
            self._newfile(name)
        path = '/'+self.list[name][1]+'/'+str(self.list[name][2]+1)
        hint = 'Please input the texts here (End with a blank line): '
        if input('Enter "y" to comfirm:')!='y':
            return None
        self.dbt.write(m_input(hint),path)
        self.list[name][2] += 1
        self.write_list()
    def _newfile(self,name):
        print('This is a new file.')
        des = input('Description:')
        md = hashlib.md5(name.encode()).hexdigest()
        self.list[name] = [des,md,-1]

def m_input(t):
    lines = []
    while True:
        line = input(t)
        t=''
        if line:
            lines.append(line)
        else:
            break
    return('\n'.join(lines))

def input_token():
    print('Now I need to save your Dropbox token.')
    print('First, set a new password for storing any infomation.')
    print('Please be sure to remember the password!!!')
    aes = AESCipher()
    print('Please input again.')
    aes2 = AESCipher()
    if aes.key != aes2.key:
        print('Not same password.')
        exit
    token = aes.encrypt(input('Dropbox token: '))
    with open('token','wb') as f:
        f.write(token)

###############################

if not os.path.exists('token'):
    input_token()
with open('token','rb') as f:
    token = f.read()
rcd = recorder(token)
rcd.print_list()
while True:
    c = input('>>> ')
    if c=='exit':
        break
    elif c=='token':
        input_token()
    else:
        cs = c.split()
        if cs[0]=='show':
            rcd.show(cs[1])
        elif cs[0]=='list':
            rcd.print_list()
        elif cs[0]=='write':
            rcd.write(cs[1])