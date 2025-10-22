from django.db import models

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.name} - {self.date}"

