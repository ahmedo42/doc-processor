# PDF and Image Processing API

A Django REST API for handling PDF and image file operations, including uploads, rotations, and PDF to image conversions.


## Project Structure

doc-processor/
│
├── api/
│   ├── migrations/
│   ├── test_files/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
| 
├── processor/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
|
├── .pre-commit-config.yaml/
├── Dockerfile
├── docker-compose.yaml
├── Document Processor.postman_collection.json
├── manage.py
├── requirements.txt
└── README.md

## Features
- **File Upload** (PDF and Images)
- **Image Rotation**
- **PDF to Image Conversion**
- **List and Retrieve Files**
- **Delete Files**

## API Endpoints

### File Upload
- **POST** `/api/upload/`: Upload PDF or image files (base64 format)

### File Listing and Retrieval
- **GET** `/api/images/`: List all uploaded images
- **GET** `/api/pdfs/`: List all uploaded PDFs
- **GET** `/api/images/{id}/`: Get specific image details
- **GET** `/api/pdfs/{id}/`: Get specific PDF details

### File Deletion
- **DELETE** `/api/images/{id}/`: Delete specific image
- **DELETE** `/api/pdfs/{id}/`: Delete specific PDF

### Image Rotation
- **POST** `/api/rotate/`: Rotate an image by the specified angle

### PDF to Image Conversion
- **POST** `/api/convert-pdf-to-image/`: Convert PDF pages to images

## Prerequisites
- **Python** 3.10+
- **Docker**
- **poppler-utils** (for PDF processing)


## Installation

### Clone the Repository
```bash
git clone https://github.com/ahmedo42/doc-processor
cd doc-processor
```
### Deploy the server and run the test suite

```bash
docker compose up --build
```

