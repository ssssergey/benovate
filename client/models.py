from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inn = models.CharField(max_length=12)
    account = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def fullname(self):
        return self.user.get_full_name()

    def validate_inn(self):
        if not self.inn.isdigit():
            raise ValidationError('Все символы должны быть числовыми.')

    def save(self, *args, **kwargs):
        self.validate_inn()
        super().save(*args, **kwargs)