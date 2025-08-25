from .models import Customer
from django.db.models import Avg

class CustomerRepository:
    @staticmethod
    def all():
        return Customer.objects.all()

    @staticmethod
    def get(id):
        return Customer.objects.get(pk=id)

    @staticmethod
    def create(name, revenue):
        return Customer.objects.create(name=name, revenue=revenue)

    @staticmethod
    def average_revenue():
        return Customer.objects.aggregate(avg=Avg('revenue'))['avg']
