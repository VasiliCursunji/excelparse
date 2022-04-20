from django.db import models
from django_celery_beat.models import PeriodicTask


def upload_path(self, filename):
    return '/'.join(['files', self.resource_group_id, filename])


class BaseModel(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class ResourceList(BaseModel):
    link = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class ResourceListScanTask(PeriodicTask):
    resource_list = models.OneToOneField(ResourceList, on_delete=models.CASCADE)


class ResourceItem(BaseModel):
    hash = models.CharField(max_length=255, unique=True, primary_key=True)
    file_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    licensee = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=100, null=True)
    mimetype = models.CharField(max_length=255, null=True)
    resource_group_id = models.CharField(max_length=255, null=True)
    resource_type = models.CharField(max_length=100, null=True)
    revision_id = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    parsed = models.BooleanField(default=False)

    file = models.FileField(upload_to=upload_path)
