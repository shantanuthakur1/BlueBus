# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    duration = models.DurationField(null=True)

    def __str__(self):
        return self.source+"to"+self.dest

class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    bus_name = models.CharField(max_length=30)
    r_id = models.ForeignKey(Route, on_delete=models.SET_NULL, blank=True, null=True,)
    nos = models.DecimalField(decimal_places=0, max_digits=3)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.bus_name


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email_id = models.EmailField(max_length=30, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Book(models.Model):

    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_id = models.ForeignKey(Bus, on_delete=models.PROTECT)
    no_seats = models.DecimalField(decimal_places=0,  max_digits=3)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user_id) + "->" + str(self.bus_id)

