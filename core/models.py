from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vertical(BaseModel):
    class VerticalName(models.TextChoices):
        FEED_POST = 'feed post'

    name = models.CharField(max_length=24, choices=VerticalName)


class Service(BaseModel):
    class ServiceName(models.TextChoices):
        TUMBLR = 'tumblr'
        STRAVA = 'strava'

    name = models.CharField(max_length=240, choices=ServiceName)
    verticals = models.ManyToManyField(Vertical)


class Study(BaseModel):
    class Meta:
        verbose_name_plural = 'studies'

    name = models.CharField(max_length=240)
    authors = models.CharField(max_length=240)
    description = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service)

    def get_service(self, service_name):
        return self.services.filter(name = service_name)


class ServiceAccount(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    state = models.TextField(blank=True, null=True, unique=True)
