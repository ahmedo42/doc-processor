# models.py
import base64
import os

import PyPDF2
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


# models.py
class BaseDocument(models.Model):
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)


class ImageDocument(BaseDocument):
    width = models.IntegerField()
    height = models.IntegerField()
    channels = models.IntegerField()

    @classmethod
    def create_from_base64(cls, base64_string):
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]

        image_data = base64.b64decode(base64_string)
        file_content = ContentFile(image_data)
        img = Image.open(ContentFile(image_data))

        instance = cls(
            width=img.width,
            height=img.height,
            channels=len(img.getbands()),
            file_size=len(image_data),
        )
        instance.save()  # Save first to get the ID

        # Use ID for filename
        instance.file.save(f"{instance.id}.png", file_content, save=True)

        return instance

    class Meta:
        db_table = "Images"


class PDFDocument(BaseDocument):
    num_pages = models.IntegerField()
    page_width = models.FloatField()
    page_height = models.FloatField()

    @classmethod
    def create_from_base64(cls, base64_string):
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]

        pdf_data = base64.b64decode(base64_string)
        file_content = ContentFile(pdf_data)

        pdf = PyPDF2.PdfReader(ContentFile(pdf_data))
        first_page = pdf.pages[0]

        instance = cls(
            num_pages=len(pdf.pages),
            page_width=float(first_page.mediabox.width),
            page_height=float(first_page.mediabox.height),
            file_size=len(pdf_data),
        )
        instance.save()  # Save first to get the ID

        # Use ID for filename
        instance.file.save(f"{instance.id}.pdf", file_content, save=True)

        return instance

    class Meta:
        db_table = "Pdfs"
