import time
import json
import schedule
from bitcoin_apis.views import BitCoinExchange
import os
import requests
from rest_framework.parsers import JSONParser
import django
django.setup()
import os
import logging
from bitcoin_project import settings

log_path = os.getcwd()

LOG_PATH_ = log_path + "\\logs"

print(LOG_PATH_)

logger = logging.getLogger('Scheduler')
logger.setLevel(logging.INFO)

if not logger.handlers:

   fh=logging.FileHandler(LOG_PATH_ + "\\scheduler.log")
   logger.addHandler(fh)

settings_dict = settings.CONFIG_PATH

def run_fn():
    
   try:
        url = settings_dict['alphavantage_api_first'] + settings_dict['from_currency'] + settings_dict['alphavantage_api_second'] + \
          settings_dict['to_currency'] + settings_dict['alphavantage_api_third'] + settings_dict['secret_key']
        
        
        r = requests.get(url)
   
        data = r.json()
        
   except Exception as err:
   
     logger.error(str(err), exc_info=True)
     logger.info('-----Issue in fetch values from AlphaVantage API or Issue in the fetched data-----')
   
   
   pre_resp = data['Realtime Currency Exchange Rate']
   
   payload = {'from_currency_name': pre_resp['2. From_Currency Name'],'to_currency_name': pre_resp['4. To_Currency Name'],
              'exchange_rate': pre_resp['5. Exchange Rate'], 'last_updates_ts': pre_resp['6. Last Refreshed'], 'time_zone': pre_resp['7. Time Zone']
              }
   try:
     post_url = settings_dict['api_base_url'] + settings_dict['end_point']
     
#     logger.info(post_url)
     resp = requests.post(post_url, json=payload)
     
   except Exception as err:
   
     logger.error(str(err), exc_info=True)
     logger.info('-----Issue in posting the latest BTC price data to API-----')
   
   
   
schedule.every(60).minutes.do(run_fn)

while(True):

   schedule.run_pending()
   time.sleep(60)
