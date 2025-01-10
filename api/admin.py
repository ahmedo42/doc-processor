from django.contrib import admin

from .models import ImageDocument, PDFDocument

admin.site.register(ImageDocument)
admin.site.register(PDFDocument)
