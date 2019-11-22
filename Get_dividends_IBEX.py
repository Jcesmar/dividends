#!/usr/bin/env python
# coding: utf-8

# Designed by ARH.
# ticker = 'BBVA';

import os, sys
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

ticker = sys.argv[1]
print('****************************')
print('* Reading ticker: {0}.'.format(ticker))

# We define the global url from investing equities
URL_INIT = 'https://es.investing.com/equities/'

# We define a dictionary that contains the tickers as well as their corresponding dividend sites.
ticker_dict = {
    'ANA': 'acciona-sa-dividends/',  
    'ACX': 'acerinox-dividends/',
    'ACS': 'acs-cons-y-serv-dividends/',
    'AENA': 'aena-aeropuertos-sa-dividends/',
    'AMA': 'amadeus-dividends/',
    'MTS': 'arcelormittal-reg-dividends?cid=32439/',
    'SABE': 'bco-de-sabadell-dividends/',
    'BKIA': 'bankia-dividends/',
    'BKT': 'bankinter-dividends/',
    'BBVA': 'bbva-dividends/',
    'CABK': 'caixabank-sa-dividends/',
    'CLNX': 'cellnex-telecom-dividends/',
    'CIEA': 'cie-automotive-sa-dividends/',
    'COL': 'inmob-colonial-dividends/',    
    'ENAG': 'enagas-dividends/',
    'ENC': 'ence-energia-y-celulosa-sa-dividends/',
    'ELE': 'endesa-dividends/',
    'FER': 'grupo-ferrovial-dividends/',
    'GRLS': 'grifols-dividends/',
    'ICAG': 'intl.-cons.-air-grp-dividends?cid=13809/',
    'IBE': 'iberdrola-dividends/',
    'ITX': 'inditex-dividends/',
    'IDR': 'indra-sistemas-dividends/',
    'MAP': 'mapfre-dividends/',
    'MASM': 'world-wide-web-ibercom-s.a.-dividends/',
    'TL5': 'mediaset-esp-dividends/',
    'MEL': 'melia-hotels-international-sa-dividends/',
    'MRL': 'merlin-properties-sa-dividends/',
    'NTGY': 'gas-natural-sdg-dividends/',
    'REE': 'red-electrica-dividends/',
    'REP': 'repsol-ypf-dividends/',
    'SAN': 'banco-santander-dividends/',
    'SGREN': 'gamesa-dividends/',
    'TEF': 'telefonica-dividends/',
    'VIS': 'viscofan-sa-dividends/',   
}

# We define the url and the agent that will allow to download the html file.
url = os.path.join(URL_INIT, ticker_dict[ticker])
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = url

print('* Downloading webpage.')
# We make the request petition to investing.
req = Request(url=reg_url, headers=headers) 
string = urlopen(req).read()

print('* Parsing HTML.')
# We use BeautifulSoup to parse the html information delivered by the website.
soup = BeautifulSoup(string, 'html.parser')
string_decoded = string.decode('utf-8');


'''
We locallize the table name directly from the html text data. The identifier will be
'<table id="dividendsHistoryDat', which is the name given to the table that contains 
dividend data.
'''
# We essentially look for our string line by line in the html text.
for i in string_decoded.split('\n'):
    if '<table id="dividendsHistoryDat' in i:
        line = i;
        
# Once we find its real identifier, we use it to get the table with all its content.
table_id = line.split('"')[1];
table = soup.find(id=table_id);


# We get the different cells available at the table
data_list = table.findAll('tr');

'''
We read the table content and store it in a dictionary. We store both the quantity and
the pay day. 
'''
pay_info = [];
for i in data_list[1:]:
    pay_info.append({
        'payday': i.findAll('td')[3].text,            
        'quantity': float(i.findAll('td')[1].text.replace(',','.')),
               })
pay_info


print('* Writing csv file.')
# We write the outcome in a text file.
import csv
csv_file = "{0}_dividends.csv".format(ticker)
csv_columns = ['quantity', 'payday']
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in pay_info:
            writer.writerow(data)
except IOError:
    print("I/O error") 
print('****************************')
