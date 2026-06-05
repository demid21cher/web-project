from django.db import models
from django.contrib.auth.models import User


class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    description = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.city} - {self.temperature}°C, {self.humidity}% humidity, {self.description}"


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, default="")
    search_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-search_date"]
        indexes = [
            models.Index(fields=["user", "-search_date"]),
        ]

    def __str__(self):
        return f"{self.user.username} search {self.city} - {self.search_date}"
