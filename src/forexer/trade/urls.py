from django.urls import path, include

from forexer.trade.views import (
    TradeListView,
    TradeCreateView,
    tradequote,
    available_currencies,
)


urlpatterns = [
    path('', TradeListView.as_view(), name='trade-listview'),
    path('create/', TradeCreateView.as_view(), name='trade-createview'),
    path('quote/', tradequote, name='trade-quote'),
    path('available-currencies/', available_currencies, name='trade-currencies'),
]
