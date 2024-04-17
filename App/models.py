from django.contrib.auth.models import User
from django.db import models

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_credit = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_date}"