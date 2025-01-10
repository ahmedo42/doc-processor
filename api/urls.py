# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ConvertPDFToImageViewSet,
    ImageDocumentViewSet,
    PDFDocumentViewSet,
    RotateViewSet,
    UploadViewSet,
)

router = DefaultRouter()
router.register(r"images", ImageDocumentViewSet)
router.register(r"pdfs", PDFDocumentViewSet)
router.register(r"upload", UploadViewSet, basename="upload")
router.register(r"rotate", RotateViewSet, basename="rotate")
router.register(
    r"convert-pdf-to-image", ConvertPDFToImageViewSet, basename="convert-pdf-to-image"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
