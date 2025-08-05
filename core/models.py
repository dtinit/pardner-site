from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Study(BaseModel):
    class Meta:
        verbose_name_plural = 'studies'

    name = models.CharField(max_length=240)
    authors = models.CharField(max_length=240)

class ServiceAccount(BaseModel):
    class ServiceName(models.TextChoices):
        TUMBLR = 'tumblr'

    name = models.CharField(max_length=240, choices=ServiceName)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    state = models.TextField(blank=True, null=True, unique=True)

    class Meta:
        indexes = [models.Index(fields=['state'])]
