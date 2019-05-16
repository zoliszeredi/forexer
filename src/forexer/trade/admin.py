from django.contrib import admin
from forexer.trade.models import Trade


class TradeAdmin(admin.ModelAdmin):
    fields = ('id',
              'sell_currency',
              'buy_currency',
              'buy_amount',
              'sell_amount',
              'rate',
              'date_booked')
    readonly_fields = ('id', 'buy_amount', 'rate', 'date_booked')
    list_display = fields
    list_filter = ('buy_currency', 'sell_currency')
    search_fields = ('id', )

    class Meta:
        model = Trade


admin.site.register(Trade, TradeAdmin)
