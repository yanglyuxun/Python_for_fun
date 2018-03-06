#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:25:31 2017

@author: ylx
"""

import dropbox

dbx = dropbox.Dropbox('*')
dbx.users_get_current_account()

for entry in dbx.files_list_folder('').entries:
    print(entry.name)

dbx.files_upload(b"Potential headline: Game 5 a nail-biter as Warriors inch out Cavs", '/test.txt')

print(dbx.files_get_metadata('/test.txt').server_modified)
dbx.files_delete('/test.txt')

dt = dbx.files_download('/test.txt')
dt[1].content
