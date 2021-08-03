#from django.shortcuts import render

# Create your views here.
import django
django.setup()
from django.views import View
from django.http import JsonResponse
import json
from .models import BitCoinExchangeRate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os



@method_decorator(csrf_exempt, name='dispatch')
class BitCoinExchange(View):

    
    
    def post(self, request):
        
#        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitcoin_project.settings')
#        obj = BitCoinExchange().post()
        data = json.loads(request.body.decode("utf-8"))
        from_currency_name = data.get('from_currency_name')
        to_currency_name = data.get('to_currency_name')
        exchange_rate = data.get('exchange_rate')
        last_updates_ts = data.get('last_updates_ts')
        time_zone = data.get('time_zone')
        
        

        product_data = {
            'from_currency_name': from_currency_name,
            'to_currency_name': to_currency_name,
            'exchange_rate': exchange_rate,
            'last_updates_ts': last_updates_ts,
            'time_zone': time_zone,
        }
 
        try:
        
            bitcoin_exchangerate = BitCoinExchangeRate.objects.create(**product_data)
        
        except Exception as err:
        
           print(str(err), exc_info=True)
           print('-----Issue in inserting latest BTC data into the DB-----')
           
        data = {
           "message": f"Record with ID: {bitcoin_exchangerate.id} inserted into the DB "
        }
        
        
        return JsonResponse(data, status=201)
        
    

    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request):
        
       # items = BitCoinExchangeRate.objects.all()
       
        try:
        
            items = BitCoinExchangeRate.objects.last()
        
        except Exception as err:
        
           print(str(err), exc_info=True)
           print('-----Issue in fetching the latest BTC data from the DB-----')
           
        items_data = []
        
        #for item in items:
        
        items_data.append({
                'from_currency_name': items.from_currency_name,
                'to_currency_name': items.to_currency_name,
                'exchange_rate': items.exchange_rate,
                'last_updates_ts': items.last_updates_ts,
                'time_zone': items.time_zone,
                
                
            })

        data = {
            'items': items_data,
        }

        return JsonResponse(data)
