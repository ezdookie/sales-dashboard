from django.urls import path

from apps.sales.views import SubscriptionListView, SubscriptionCreateView

app_name = 'sales'

urlpatterns = [
    path('', SubscriptionListView.as_view(), name='subscription-list'),
    path('new/', SubscriptionCreateView.as_view(), name='subscription-create'),
]
