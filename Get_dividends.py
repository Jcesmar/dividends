#!/usr/bin/env python
# coding: utf-8

# Author JCM.
# Thanks to ARH for base code
# ticker = 'BBVA';

import os,sys
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)   

ch = logging.StreamHandler()
ch.setLevel(logging.INFO) # or any other level
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.addHandler(ch) 
fh = logging.FileHandler('/Users/jcespedes/Documents/GitHub/dividends/myLog.log')
fh.setLevel(logging.DEBUG) # or any level you want
logger.addHandler(fh)
now=dt.datetime.now()
logger.debug("******************************")
logger.debug("Updated at:{}".format( now.strftime("%m/%d/%Y, %H:%M:%S")))

pay_info = [];
# use creds to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jcespedes/Documents/GitHub/dividends/client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the interest_sheet 
# Make sure you use the right name here.
read_sheet=1
write_sheet=3
sheets = client.open("Historico Diviendos").worksheets()
data=sheets[read_sheet].get_all_records() 
logger.debug("Data Sheet Readed")
# We define the global url from investing equities
URL_INIT = 'https://es.investing.com/equities/'
for index,company in enumerate(data):
    # We define the url and the agent that will allow to download the html file.
    #firstly checking if it has the correct format
    if "investing.com/equities/" not in data[index]['partial']:
        url = os.path.join(URL_INIT, data[index]['partial'])
    else:
        url=os.path(data[index]['partial'])
        
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = url
    
    logging.debug('Downloading company info!')
    # We make the request petition to investing.
    req = Request(url=reg_url, headers=headers) 
    string = urlopen(req).read()
    
    logging.debug('* Parsing HTML.')
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
        logging.debug("Sin dividendo")
    

logging.debug('* Updating Sheet.')
# We write the outcome in a the write_sheet.
now = dt.datetime.now()
sheets[write_sheet].clear()
second_row = ['Company','Ticker','Quantity','Currency', 'Payday','Quantity in EUR at Payday']
sheets[write_sheet].insert_row(["Updated at:", now.strftime("%m/%d/%Y, %H:%M")], index=1)
sheets[write_sheet].insert_row(second_row, index=2)
sheets[write_sheet].append_rows(pay_info,value_input_option="USER_ENTERED")

logging.debug("Done! at {}".format( now.strftime("%m/%d/%Y, %H:%M:%S")))