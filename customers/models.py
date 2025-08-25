from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    revenue = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.revenue})"
