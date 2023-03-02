from django.db import models


# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.FloatField()
    mileage = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    image_url = models.URLField()


class Feature(models.Model):
    name = models.CharField(max_length=255)


class CarFeature(models.Model):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    feature = models.ForeignKey("Feature", on_delete=models.CASCADE)
