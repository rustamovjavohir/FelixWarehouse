from django.urls import path, include

from api.factory import urls as factory_urls

urlpatterns = [
    path('', include(factory_urls)),
]
