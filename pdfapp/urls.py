from django.urls import path

from pdfapp.views import UploadPDFView

urlpatterns = [
    path('upload/', UploadPDFView.as_view(), name='upload-pdf'),
]
