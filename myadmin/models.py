from django.db import models

class Category(models.Model):   
    catid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=50,unique=True)
    caticonnm=models.CharField(max_length=100)

class SubCategory(models.Model):   
    subcatid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=50)
    subcatnm=models.CharField(max_length=50,unique=True)
    subcaticonnm=models.CharField(max_length=100)    
