import pytest

from forexer.rates import api


@pytest.mark.parametrize(
    "rates", [api.DummyRates, api.FixerRates, api.Rates]
)
def test_currencies(rates):
    actual = rates.currencies()
    currencies = {'USD', 'EUR', 'GBP', 'JPY', 'CNY'}
    assert currencies.issubset(actual)


def test_operations():
    input_data = {
        'sell_currency': 'EUR',
        'buy_currency': 'GBP',
        'sell_amount': '0.1',
    }
    expected = {
        'sell_amount': '0.1',
        'buy_amount': '0.09',
        'sell_currency': 'EUR',
        'buy_currency': 'GBP',
        'rate': '0.8672',
    }
    op = api.MarketOperation(**input_data)
    op._rates = api.DummyRates  # don't do IO
    assert op.as_dict() == input_data
    assert op.as_dict(force_evaluation=True) == expected


@pytest.mark.parametrize(
    "input_data,expected_message", [
        [
            {
                'sell_currency': 'XXX',
                'buy_currency': 'GBP',
                'sell_amount': '1.0',
            },
            "Sell Currency XXX"
        ],
        [
            {
                'sell_currency': 'EUR',
                'buy_currency': 'XXX',
                'sell_amount': '1.0',
            },
            "Buy Currency XXX"
        ]
    ]
)
def test_validation(input_data, expected_message):
    op = api.MarketOperation(**input_data)
    with pytest.raises(ValueError) as excinfo:
        op.validate()
    assert expected_message in str(excinfo.value)


def test_todecimal():
    assert api.to_decimal(0.1) == api.to_decimal('0.1')


def test_repr():
    input_data = {
        'sell_currency': 'EUR',
        'buy_currency': 'GBP',
        'sell_amount': '1.0',
    }
    op = api.MarketOperation(**input_data)
    assert repr(op) == ('MarketOperation('
                        'sell_currency="EUR", '
                        'sell_amount="1.0", '
                        'buy_currency="GBP")')
    op._rates = api.DummyRates
    op.as_dict(force_evaluation=True)
    assert repr(op) == ('MarketOperation('
                        'sell_currency="EUR", '
                        'sell_amount="1.0", '
                        'buy_currency="GBP", '
                        'buy_amount="0.87", '
                        'rate="0.8672")')
