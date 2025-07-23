from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    @classmethod
    def create(cls, created_by):
        return cls(created_by=created_by)


class Study(BaseModel):
    class Meta:
        verbose_name_plural = 'studies'

    name = models.CharField(max_length=240)
    authors = models.CharField(max_length=240)
