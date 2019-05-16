import logging
import datetime
import xml.etree.ElementTree
import os

import requests


ACCESS_KEY = os.getenv('FIXER_KEY', '')


if os.getenv('LOGLEVEL'):
    logging.basicConfig(
        level=getattr(logging, os.getenv('LOGLEVEL').upper())
    )


def http_get(url):
    response = requests.get(url, timeout=3)
    logging.log(logging.INFO, 'request.get %s', url)
    return response


def ecb():
    """See
    https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html
    """
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    response = http_get(url)
    tree = xml.etree.ElementTree.fromstring(response.content)
    ns = r'{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}'
    node = '{ns}Cube'.format(ns=ns)
    items = tree.find(node).find(node).findall(node)
    date = tree.find(node).find(node).attrib['time']
    timestamp = datetime.datetime.now().timestamp()
    result = {
        'timestamp': timestamp,
        'date': date,
        'success': True,
        'base': 'EUR',
        'rates': {
            element.attrib['currency']: element.attrib['rate']
            for element in items
        }
    }
    result['rates']['EUR'] = 1.0
    return result


def fixer():
    url = 'http://data.fixer.io/api/latest?access_key={key}'.format(
        key=ACCESS_KEY
    )
    response = http_get(url)
    data = response.json()
    data['rates']['EUR'] = 1.0
    return data


def dummy():
    result = {
        'timestamp': 1557884588,
        'date': '2019-05-15',
        'success': True,
        'base': 'EUR',
        'rates': {
            'EUR': '1.0000',
            'USD': '1.1226',
            'AUD': '1.6162',
            'GBP': '0.86723',
            'JPY': '123.00',
            'CHF': '1.1307',
            'CAD': '1.5117',
            'CNY': '7.7252',
        }
    }
    return result
