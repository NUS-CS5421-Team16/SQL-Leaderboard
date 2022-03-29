from django.db import models


def get_upload_competitor_info_path(instance, filename):
    return f"competition_{instance.name}_conf/competitor_info.txt"


def get_upload_private_path(instance, filename):
    return f"competition_{instance.name}_conf/private.sql"


def get_upload_public_path(instance, filename):
    return f"competition_{instance.name}_conf/public.sql"


def get_reference_query_path(instance, filename):
    return f"competition_{instance.name}_conf/reference.sql"


class Competition(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    upload_limit = models.IntegerField(blank=False, null=False)
    running_time_limit = models.IntegerField(blank=False, null=False)
    concurrent_limit = models.IntegerField(blank=False, null=False, default=1)
    end_time = models.DateTimeField(blank=False, null=False)
    competitor_info = models.FileField(upload_to=get_upload_competitor_info_path, blank=False, null=False)
    private_sql = models.FileField(upload_to=get_upload_private_path, blank=False, null=False)
    public_sql = models.FileField(upload_to=get_upload_public_path, blank=False, null=False)
    reference_query = models.FileField(upload_to=get_reference_query_path, blank=False, null=False)
    private_result = models.TextField(null=True)
    public_result = models.TextField(null=True)
    descendent_ordering = models.BooleanField(blank=False, null=False)




