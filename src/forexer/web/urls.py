from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import routers

import forexer.trade.views

router = routers.DefaultRouter()
router.register(r'trades', forexer.trade.views.TradeViewSet)


urlpatterns = [
    path('djangoapp/', include('forexer.trade.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT) if settings.DEBUG else []
