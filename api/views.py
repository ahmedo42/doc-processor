# views.py
import base64
import io

import pdf2image
from PIL import Image
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ImageDocument, PDFDocument
from .serializers import (
    ImageDocumentSerializer,
    PDFDocumentSerializer,
    PDFToImageSerializer,
    RotateImageSerializer,
    UploadSerializer,
)


class ImageDocumentViewSet(viewsets.ModelViewSet):
    queryset = ImageDocument.objects.all()
    serializer_class = ImageDocumentSerializer


class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer


class UploadViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            base64_file = serializer.validated_data["file"]

            try:
                # Check if it's a PDF by looking at the base64 header
                if "data:application/pdf" in base64_file:
                    document = PDFDocument.create_from_base64(base64_file)
                    return Response(PDFDocumentSerializer(document).data)
                else:
                    # Assume it's an image
                    document = ImageDocument.create_from_base64(base64_file)
                    return Response(ImageDocumentSerializer(document).data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RotateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RotateImageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image_doc = ImageDocument.objects.get(
                    id=serializer.validated_data["image_id"]
                )
                img = Image.open(image_doc.file)
                rotated_img = img.rotate(serializer.validated_data["angle"])

                # Save rotated image to bytes
                img_byte_arr = io.BytesIO()
                rotated_img.save(img_byte_arr, format="PNG")
                img_byte_arr = img_byte_arr.getvalue()

                # Convert to base64
                base64_image = base64.b64encode(img_byte_arr).decode()

                return Response({"rotated_image": base64_image})
            except ImageDocument.DoesNotExist:
                return Response(
                    {"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConvertPDFToImageViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PDFToImageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pdf_doc = PDFDocument.objects.get(
                    id=serializer.validated_data["pdf_id"]
                )
                images = pdf2image.convert_from_path(pdf_doc.file.path)

                # Convert all pages to base64
                base64_images = []
                for i, image in enumerate(images):
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format="PNG")
                    img_byte_arr = img_byte_arr.getvalue()

                    # Convert to base64
                    base64_image = base64.b64encode(img_byte_arr).decode()
                    base64_images.append({"page": i + 1, "image": base64_image})

                return Response(
                    {"total_pages": len(base64_images), "images": base64_images}
                )
            except PDFDocument.DoesNotExist:
                return Response(
                    {"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
