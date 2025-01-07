from django.db import models


class Resource(models.Model):
    id = models.BigAutoField(primary_key=True)
    resource_path = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    resource = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name="image"
    )
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    channels = models.PositiveSmallIntegerField()


class Pdf(models.Model):
    resource = models.OneToOneField(
        Resource, on_delete=models.CASCADE, related_name="pdf"
    )
    page_width = models.PositiveSmallIntegerField()
    page_height = models.PositiveSmallIntegerField()
    pages = models.PositiveIntegerField()
