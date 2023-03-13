from odoo import http
from odoo.http import request
from requests_cache import CachedSession
import requests
import jwt

class Authentication(http.Controller):
    @http.route('/fetch', type='json', auth="public", methods=['GET'], csrf=False)
    def fetch(self, **params):
        api_key = request.httprequest.headers.get("Authorization")
        token = api_key.split(" ")
        decoded = jwt.decode(token[1] or "", "PLACE_SECRET_HERE_SOON", algorithms="HS256")

        # Cache
        session = CachedSession('example_cache', 'memory')

        # Get Currency Rates
        currency_endpoint = 'https://api.apilayer.com/exchangerates_data/convert?to=IDR&from=USD&amount=1'
        headers = {'apikey' : 'jkek1Z5g7I82rVzu6QdmLbg6aaMRzubZ'}
        # Caching request
        currency_result = session.get(currency_endpoint, headers=headers).json()
        rates = currency_result.get('result')
        
        # Fetch data
        endpoint = 'https://stein.efishery.com/v1/storages/5e1edf521073e315924ceab4/list'
        result = requests.get(endpoint).json()
        for res in result:
            res['usd'] = int(res.get('price') or 0) /rates
        return result
        