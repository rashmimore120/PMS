from django.db import models

# Create your models here.

class Payment(models.Model):   
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=100)
    amount=models.CharField(max_length=20)
    info=models.CharField(max_length=100)
