from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Expense(models.Model):
    CATEGORY_CHOICES=[
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Other', 'Other')
    ]

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description=models.TextField(blank=True)
    date=models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount}"

