from django.urls import path
from .api import AverageRevenueAPIView
from .views import add_customer, customer_list

urlpatterns = [
    path('average-revenue/', AverageRevenueAPIView.as_view(), name='average-revenue'),
    path('customers/add/', add_customer, name='add_customer'),
    path('customers/', customer_list, name='customer_list'),
]