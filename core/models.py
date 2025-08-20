from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session

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


class ServiceAccountManager(models.Manager):
    def get_or_create_from_session(self, study_id, session_id, service_id):
        potential_service_accounts = self.filter(
            study__pk=study_id, session__pk=session_id, service__pk=service_id
        )
        if potential_service_accounts.count() == 0:
            service_account = ServiceAccount(
                study_id=study_id, session_id=session_id, service_id=service_id
            )
            service_account.save()
            return service_account

        return potential_service_accounts.last()


class ServiceAccount(BaseModel):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    state = models.TextField(blank=True, null=True, unique=True)
    completed_donation_at = models.DateTimeField(blank=True, null=True)

    objects = ServiceAccountManager()

    @property
    def has_completed_donation(self):
        return (
            self.completed_donation_at < timezone.now()
            if self.completed_donation_at
            else False
        )
