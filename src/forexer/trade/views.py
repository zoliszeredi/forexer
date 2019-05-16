import collections

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView


from rest_framework import (
    viewsets,
    serializers,
)

from forexer.trade.models import Trade
from forexer.rates import api


class TradeSerializer(serializers.HyperlinkedModelSerializer):
    date_booked = serializers.DateTimeField(format="%d/%m/%Y %H:%M",
                                            read_only=True)

    def to_internal_value(self, data):
        operation = api.MarketOperation(
            sell_currency=data['sell_currency'],
            sell_amount=data['sell_amount'],
            buy_currency=data['buy_currency'],
        )
        result = operation.as_dict(force_evaluation=True)
        return result


    class Meta:
        model = Trade
        fields = ('id',
                  'sell_currency',
                  'buy_currency',
                  'buy_amount',
                  'sell_amount',
                  'rate',
                  'date_booked')


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class TradeListView(ListView):
    model = Trade
    paginate_by = 15


class TradeCreateView(CreateView):
    model = Trade
    fields = ['sell_currency',
              'sell_amount',
              'buy_currency']
    success_url = reverse_lazy('trade-listview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currencies'] = api.Rates.currencies()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            trade = form.save()
            operation = api.MarketOperation(
                sell_currency=trade.sell_currency,
                sell_amount=trade.sell_amount,
                buy_currency=trade.buy_currency,
            )
            trade.rate = operation.rate
            trade.buy_amount = operation.buy_amount
            trade.save()
            response = HttpResponseRedirect(self.success_url)
        else:
            response = render(
                request,
                'trade/trade_form.html',
                {'form': form}
            )
        return response


def available_currencies(request):
    currencies = api.Rates.currencies()
    data = {'currencies': list(currencies)}
    response = JsonResponse(data)
    return response


def tradequote(request):
    operation = api.MarketOperation(
        sell_currency=request.GET.get('sell_currency'),
        sell_amount=request.GET.get('sell_amount'),
        buy_currency=request.GET.get('buy_currency'),
    )
    try:
        data = operation.as_dict(force_evaluation=True)
        status_code = 200
    except ValueError as e:
        data = {'error': str(e)}
        status_code = 400
    response = JsonResponse(data, status=status_code)
    return response
