from djongo import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def get_default_user():
    return User.objects.first().pk

# Create your models here.
class userPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user())
    currency = models.CharField(max_length=3, null= True , default='BHD')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + 's preferences'