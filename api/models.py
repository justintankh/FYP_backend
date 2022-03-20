from django.db import models
import string
import random


def generate_unique_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Owner.objects.filter(code=code).count() == 0:
            break
    return code


def generate_unique_p_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Perishable.objects.filter(p_code=code).count() == 0:
            break
    return code


class Owner(models.Model):
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=20, default="")
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)


class Perishable(models.Model):
    username = models.CharField(max_length=20, unique=False, null=False)
    p_code = models.CharField(
        max_length=8, default=generate_unique_p_code, unique=True)
    title = models.CharField(max_length=200, null=False)
    img_url = models.CharField(max_length=1000, null=False)
    # Fields that might not exist
    b_code = models.CharField(max_length=200, default='EMPTY')
    categories = models.CharField(max_length=1000, null=False, default='')
    categories_score = models.CharField(
        max_length=5000, null=False, default='')
    qty = models.IntegerField(null=False, default=1)
    rtr_date = models.DateField(auto_now_add=True)
    exp = models.DateField()
