from django.db import models


class Asset(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    activation_cost = models.FloatField()
    volume = models.IntegerField()
    # reverse foreign key availabilities

    def __str__(self):
        return f"{self.name} (volume: {self.volume}, activation_cost: {self.activation_cost})"


class Availability(models.Model):

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
