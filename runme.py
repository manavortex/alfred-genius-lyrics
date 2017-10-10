#!/usr/bin/python
# encoding: utf-8

import sys  
import re
import urllib2
import json
import csv
import codecs
import os
import socket
from workflow import (Workflow3, ICON_INFO, ICON_WARNING, ICON_ERROR,
                      ICON_SETTINGS, ICON_SYNC)
from workflow.background import is_running, run_in_background
from cache import cache_key

UPDATE_SETTINGS = {'github_slug': 'manavortex/alfred-genius-lyrics'}


def search(search_term):
    querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_term)
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + "XrgFo2k9c6FR0x1nNimiHfHyzHqNSth10zhj1Jtwhxkai1qNtG_rvkAGUQl_uF1X")   
    request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
    while True:
        try:
            response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
            raw = response.read()
        except socket.timeout:
            print("Timeout raised and caught")
            continue
        break
    json_obj = json.loads(raw)
    body = json_obj["response"]["hits"]
    return body
    
           
    


if __name__ == '__main__':

    wf = Workflow3(update_settings=UPDATE_SETTINGS)
    log = wf.logger
    sf = SmartFolders()
    sys.exit(wf.run(sf.run))

    alfred.work(volatile=False)
    
    record = alfred.args()
    if len(record) > 0 and len(record[0]) > 1 and record[0][1]:
        (query) = alfred.args()[0] # proper decoding and unescaping of command line arguments
    else:
        query = "autoset"
    

    
    body = search(query)
    results = []
    for result in body:
        header_image_url = result["result"]["header_image_url"]
        item = alfred.Item({'arg': result["result"]["url"], 'valid': 'yes'}, result["result"]["title"], result["result"]["primary_artist"]["name"], (header_image_url, {'type': 'filetype'}))
    
    xml = alfred.xml(results)
    alfred.write(xml) 