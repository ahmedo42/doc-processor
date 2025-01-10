# api/tests.py
import base64
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ImageDocument, PDFDocument

class FileUploadTests(APITestCase):
    def setUp(self):
        # Create test files in memory
        self.test_image_path = 'api/test_files/test_image.png'
        self.test_pdf_path = 'api/test_files/test_document.pdf'
        
        # Create base64 strings for testing
        with open(self.test_image_path, 'rb') as image_file:
            self.image_base64 = base64.b64encode(image_file.read()).decode()
        
        with open(self.test_pdf_path, 'rb') as pdf_file:
            self.pdf_base64 = base64.b64encode(pdf_file.read()).decode()

    def test_upload_image(self):
        """
        Test uploading an image file.
        """
        url = reverse('upload-list')
        data = {
            'file': f'data:image/png;base64,{self.image_base64}'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ImageDocument.objects.exists())

    def test_upload_pdf(self):
        """
        Test uploading a PDF file.
        """
        url = reverse('upload-list')
        data = {
            'file': f'data:application/pdf;base64,{self.pdf_base64}'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PDFDocument.objects.exists())

    def test_upload_invalid_base64(self):
        """
        Test uploading invalid base64 data.
        """
        url = reverse('upload-list')
        data = {
            'file': 'invalid_base64_string'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ImageDocumentTests(APITestCase):
    def setUp(self):
        # Create a test image document
        with open('api/test_files/test_image.png', 'rb') as image_file:
            base64_string = base64.b64encode(image_file.read()).decode()
            self.image_doc = ImageDocument.create_from_base64(base64_string)

    def test_list_images(self):
        """
        Test retrieving list of images.
        """
        url = reverse('imagedocument-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_image(self):
        """
        Test retrieving a specific image.
        """
        url = reverse('imagedocument-detail', args=[self.image_doc.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.image_doc.id)

    def test_delete_image(self):
        """
        Test deleting an image.
        """
        url = reverse('imagedocument-detail', args=[self.image_doc.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ImageDocument.objects.exists())

class RotateTests(APITestCase):
    def setUp(self):
        # Create a test image document
        with open('api/test_files/test_image.png', 'rb') as image_file:
            base64_string = base64.b64encode(image_file.read()).decode()
            self.image_doc = ImageDocument.create_from_base64(base64_string)

    def test_rotate_image(self):
        """
        Test rotating an image.
        """
        url = reverse('rotate-list')
        data = {
            'image_id': self.image_doc.id,
            'angle': 90
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rotated_image', response.data)

    def test_rotate_nonexistent_image(self):
        """
        Test rotating a non-existent image.
        """
        url = reverse('rotate-list')
        data = {
            'image_id': 999,
            'angle': 90
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ConvertPDFTests(APITestCase):
    def setUp(self):
        # Create a test PDF document
        with open('api/test_files/test_document.pdf', 'rb') as pdf_file:
            base64_string = base64.b64encode(pdf_file.read()).decode()
            self.pdf_doc = PDFDocument.create_from_base64(base64_string)

    def test_convert_pdf_to_image(self):
        """
        Test converting PDF to images.
        """
        url = reverse('convert-pdf-to-image-list')
        data = {
            'pdf_id': self.pdf_doc.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_pages', response.data)
        self.assertIn('images', response.data)
        self.assertTrue(isinstance(response.data['images'], list))
        self.assertTrue(all(
            'page' in image and 'image' in image 
            for image in response.data['images']
        ))

    def test_convert_nonexistent_pdf(self):
        """
        Test converting a non-existent PDF.
        """
        url = reverse('convert-pdf-to-image-list')
        data = {
            'pdf_id': 999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)