#!/usr/bin/env python
# coding: utf-8

# Designed by ARH.
# Re-Designed by JCM
# ticker = 'BBVA';

import os, sys
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
from crontab import CronTab


print('****************************')
print('* Reading ...')

# We define the global url from investing equities
URL_INIT = 'https://es.investing.com/equities/'

# We define a dictionary that contains the tickers as well as their corresponding dividend sites.
#ticker_dict = {
#'BME:ANA': {'parcial': 'acciona-sa-dividends/', 'divisa':'EUR'},
#'BME:ACX': {'parcial': 'acerinox-dividends/', 'divisa':'EUR'},
#'BME:ACS': {'parcial': 'acs-cons-y-serv-dividends/', 'divisa':'EUR'},
#'BME:AENA': {'parcial': 'aena-aeropuertos-sa-dividends/', 'divisa':'EUR'},
#'BME:AMS': {'parcial': 'amadeus-dividends/', 'divisa':'EUR'},
#'BME:MTS': {'parcial': 'arcelormittal-reg-dividends?cid=32439/', 'divisa':'EUR'},
#'BME:SAB': {'parcial': 'bco-de-sabadell-dividends/', 'divisa':'EUR'},
#'BME:BKIA': {'parcial': 'bankia-dividends/', 'divisa':'EUR'},
#'BME:BKT': {'parcial': 'bankinter-dividends/', 'divisa':'EUR'},
#'BME:BBVA': {'parcial': 'bbva-dividends', 'divisa':'EUR'},
#'BME:CABK': {'parcial': 'caixabank-sa-dividends/', 'divisa':'EUR'},
#'BME:CLNX': {'parcial': 'cellnex-telecom-dividends', 'divisa':'EUR'},
#'BME:CIE': {'parcial': 'cie-automotive-sa-dividends', 'divisa':'EUR'},
#'BME:COL': {'parcial': 'inmob-colonial-dividends', 'divisa':'EUR'},
#'BME:ENG': {'parcial': 'enagas-dividends', 'divisa':'EUR'},
#'BME:ENC': {'parcial': 'ence-energia-y-celulosa-sa-dividends', 'divisa':'EUR'},
#'BME:ELE': {'parcial': 'endesa-dividends', 'divisa':'EUR'},
#'BME:FER': {'parcial': 'grupo-ferrovial-dividends', 'divisa':'EUR'},
#'BME:GRF': {'parcial': 'grifols-dividends', 'divisa':'EUR'},
#'BME:IAG': {'parcial': 'intl.-cons.-air-grp-dividends?cid=13809', 'divisa':'EUR'},
#'BME:IBE': {'parcial': 'iberdrola-dividends', 'divisa':'EUR'},
#'BME:ITX': {'parcial': 'inditex-dividends', 'divisa':'EUR'},
#'BME:IDR': {'parcial': 'indra-sistemas-dividends', 'divisa':'EUR'},
#'BME:MAP': {'parcial': 'mapfre-dividends', 'divisa':'EUR'},
#'BME:MASM': {'parcial': 'world-wide-web-ibercom-s.a.-dividends', 'divisa':'EUR'},
#'BME:TL5': {'parcial': 'mediaset-esp-dividends', 'divisa':'EUR'},
#'BME:MEL': {'parcial': 'melia-hotels-international-sa-dividends', 'divisa':'EUR'},
#'BME:MRL': {'parcial': 'merlin-properties-sa-dividends', 'divisa':'EUR'},
#'BME:NTGY': {'parcial': 'gas-natural-sdg-dividends', 'divisa':'EUR'},
#'BME:REE': {'parcial': 'red-electrica-dividends', 'divisa':'EUR'},
#'BME:REP': {'parcial': 'repsol-ypf-dividends', 'divisa':'EUR'},
#'BME:SAN': {'parcial': 'banco-santander-dividends', 'divisa':'EUR'},
#'BME:SGRE': {'parcial': 'gamesa-dividends', 'divisa':'EUR'},
#'BME:TEF': {'parcial': 'telefonica-dividends', 'divisa':'EUR'},
#'BME:VIS': {'parcial': 'viscofan-sa-dividends', 'divisa':'EUR'},
#'BME:ALTN': {'parcial': 'dinamia-capital-privado-scr-sa-dividends', 'divisa':'EUR'},
#}
#tickers=ticker_dict.keys()
pay_info = [];
# use creds to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the interest_sheet 
# Make sure you use the right name here.
read_sheet=1
write_sheet=3
sheets = client.open("Historico Diviendos").worksheets()
data=sheets[read_sheet].get_all_records() 

for index,company in enumerate(data):
    # We define the url and the agent that will allow to download the html file.
    if "investing.com/equities/" not in data[index]['partial']:
        url = os.path.join(URL_INIT, data[index]['partial'])
    else:
        url=os.path(data[index]['partial'])
        
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
    
    try:
    # We get the different cells available at the table
        data_list = table.findAll('tr');
        
        '''
        We read the table content and store it in a dictionary. We store both the quantity and
        the pay day. 
        '''
        
        for i in data_list[1:]:
            pay_info.append(
                [ '=GOOGLEFINANCE("'+data[index]['Ticker']+ '";\"name\")',
                 data[index]['Ticker'],
                 float(i.findAll('td')[1].text.replace(',','.')) ,data[index]['Divisa'],
                 i.findAll('td')[3].text.replace('.','/')])
                    
    except AttributeError:
        print("Sin dividendo")
    

print('* Updating Sheet.')
# We write the outcome in a the write_sheet.
now = dt.datetime.now()
sheets[write_sheet].clear()
second_row = ['Company','Ticker','Quantity','Currency', 'Payday','Quantity in EUR']
sheets[write_sheet].insert_row(["Updated at:", now.strftime("%m/%d/%Y, %H:%M")], index=1)
sheets[write_sheet].insert_row(second_row, index=2)
sheets[write_sheet].append_rows(pay_info,value_input_option="USER_ENTERED")

#try:
#    with open(csv_file, 'w') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames=csv_columns,delimiter=";")
#        writer.writeheader()
#        for data in pay_info:
#            writer.writerow(data)
#except IOError:
#    print("I/O error") 
print('****************************')
