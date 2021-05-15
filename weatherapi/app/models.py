from djongo import models


class Weather(models.Model):
    main = models.CharField(max_length=10)
    description = models.CharField(max_length=25)
    icon = models.CharField(max_length=5)

    class Meta:
        abstract = True


class WeatherData(models.Model):
    dt = models.IntegerField()
    temp = models.FloatField()
    feels_like = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    dew_point = models.FloatField()
    uvi = models.SmallIntegerField()
    clouds = models.SmallIntegerField()
    visibility = models.IntegerField()
    wind_speed = models.FloatField()
    wind_deg = models.SmallIntegerField()
    weather = models.ArrayField(model_container=Weather)

    class Meta:
        abstract = True


# Create your models here.
class HourlyData(models.Model):
    name = models.CharField(max_length=20)
    lat = models.FloatField()
    lon = models.FloatField()
    timezone = models.CharField(max_length=25)
    timezone_offset = models.IntegerField()
    current = models.EmbeddedField(model_container=WeatherData)
    hourly = models.ArrayField(model_container=WeatherData)
    objects = models.DjongoManager()

    def __str__(self):
        return str(self.lat) + ' ' + str(self.lon)
