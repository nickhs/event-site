#!/usr/bin/env python

import csv
import requests
import simplejson as json

nonce = 'nickisamazing'
url = "http://events.kiip.me/data"

f = open('import.csv', 'rU')

with f as cfile:
    reader = csv.reader(cfile)
    for row in reader:
        title = row[0] + " - " + row[1]
        link = row[2]
        address = row[3]
        city = "San Francisco"
        start_date = row[5]
        end_date = row[6]
        paid = row[7]
        desc = row[8]

        payload = {
            'title': title,
            'link': link,
            'address': address,
            'city': city,
            'start_date': start_date,
            'end_date': end_date,
            'paid': paid,
            'desc': desc,
            'auth': nonce,
            'owner': 'Nick'}

        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print r.text
