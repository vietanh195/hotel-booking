from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    bed_configuration = models.CharField(max_length=100)
    size = models.IntegerField()  # Size in square meters
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"