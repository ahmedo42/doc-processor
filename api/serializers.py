# serializers.py
from rest_framework import serializers

from .models import ImageDocument, PDFDocument


class ImageDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDocument
        fields = [
            "id",
            "file",
            "uploaded_at",
            "width",
            "height",
            "channels",
            "file_size",
        ]


class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = [
            "id",
            "file",
            "uploaded_at",
            "num_pages",
            "page_width",
            "page_height",
            "file_size",
        ]


class UploadSerializer(serializers.Serializer):
    file = serializers.CharField()


class RotateImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    angle = serializers.FloatField()


class PDFToImageSerializer(serializers.Serializer):
    pdf_id = serializers.IntegerField()
