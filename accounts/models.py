from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(models.User, on_delete=models.CASCADE)
    username = None
    phone = models.CharField(max_length=25, blank=True, unique=True, null=True)

    def __str__(self):
        return self.username

class Employee(models.Model):
    user = models.OneToOneField(models.User, on_delete=models.CASCADE)


# class CartItem(models.Model):


# class Cart(models.Model):
