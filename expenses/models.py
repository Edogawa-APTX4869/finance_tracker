from djongo import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
def get_default_user():
    return User.objects.first().pk

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def clean(self):
        if not self.name:
            raise ValidationError(_("The name field cannot be null or blank."))

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False)
    description = models.TextField(null=True, blank=True)  # Optional
    date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.amount <= 0:
            raise ValidationError(_("The expense amount must be greater than zero."))
        if not self.category:
            raise ValidationError(_("The expense must belong to a valid category."))

    def __str__(self):
        return f"{self.user} - ({self.amount}) - {self.category}"