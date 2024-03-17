from django.urls import path

from api.factory.views.factory import FactoryView

urlpatterns = [
    path('factory/', FactoryView.as_view(), name='factory'),
]
