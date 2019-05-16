import os
import sys
import decimal
import datetime

from forexer.rates import client


def to_decimal(val):
    "Makes sure that to_decimal(0.1) equals decimal.Decimal('0.1')"
    try:
        result = decimal.Decimal(
            repr(val) if isinstance(val, float) else val
        )
    except decimal.InvalidOperation:
        result = decimal.Decimal(0)
    return result


class Rates:
    client = getattr(client, os.getenv('RATES_CLIENT', 'ecb'))
    try:
        timeout = int(os.getenv('RATES_TIMEOUT'))
    except (ValueError, TypeError):
        timeout = 3600

    @classmethod
    def data(cls, when=None):
        current_timestamp = when or datetime.datetime.now().timestamp()
        expire_timestamp = getattr(cls, '_timestamp', 0) + cls.timeout
        if not (getattr(cls, '_data', None) is not None and
                expire_timestamp > current_timestamp):
            cls._data = cls.client()
            cls._timestamp = current_timestamp
        result = cls._data
        return result

    @classmethod
    def currencies(cls):
        result = set(cls.data()['rates'].keys())
        return result


class DummyRates(Rates):
    client = client.dummy


class FixerRates(Rates):
    client = client.fixer


class MarketOperation:
    def __init__(self, sell_currency, sell_amount,
                 buy_currency, buy_amount=None, rate=None):
        self.sell_currency = sell_currency
        self.sell_amount = sell_amount
        self.buy_currency = buy_currency
        self._buy_amount = buy_amount
        self._rate = rate
        self._client = getattr(client, os.getenv('RATES_CLIENT', 'ecb'))
        self._attribs = ('sell_currency', 'sell_amount', 'buy_currency')
        self._lazy_attribs = ('buy_amount', 'rate')

    @property
    def currencies(self):
        result = set(self.rates.keys())
        return result


    @property
    def rates(self):
        if getattr(self, '_rates', None) is None:
            self._rates = Rates
        return self._rates.data()['rates']

    def validate(self):
        if self.buy_currency not in self.currencies:
            raise ValueError(
                "Buy Currency {} not in {}".format(
                    self.buy_currency,
                    self.currencies
                )
            )
        if self.sell_currency not in self.currencies:
            raise ValueError(
                "Sell Currency {} not in {}".format(
                    self.sell_currency,
                    self.currencies
                )
            )

    @property
    def rate(self):
        self.validate()
        buy = self.rates[self.buy_currency]
        sell = self.rates[self.sell_currency]
        value = to_decimal(buy) / to_decimal(sell)
        result = round(value, 4)
        self._rate = result
        return result

    @property
    def buy_amount(self):
        value = self.rate * to_decimal(self.sell_amount)
        result = round(value, 2)
        self._buy_amount = result
        return result

    def as_dict(self, force_evaluation=False):
        lazy_attribs = ()
        if force_evaluation is False:
            for attrib in self._lazy_attribs:
                if getattr(self, '_' + attrib, None) is not None:
                    lazy_attribs = lazy_attribs + (attrib, )
        else:
            lazy_attribs = self._lazy_attribs
        data = {
            attrib : str(getattr(self, attrib))
            for attrib in self._attribs + lazy_attribs
        }
        return data

    def __repr__(self):
        data = self.as_dict()
        result = 'MarketOperation({})'.format(
            ', '.join([
                '{key}="{value}"'.format(key=key, value=value)
                for key, value in data.items()
            ])
        )
        return result
