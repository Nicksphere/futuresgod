from django.db import models

# Create user table


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=100, null=False)
    pwd = models.CharField(max_length=100, null = False)
    create_date = models.DateTimeField('date published')
    type = models.BigIntegerField(default=1)
    is_valid = models.BigIntegerField(default=1)
    belongs = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)