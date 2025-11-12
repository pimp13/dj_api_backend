from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from PyPDF2 import PdfReader
from PIL import Image
from utils.response import SuccessResponse, ErrorResponse
from .models import PDFFile
from .serializers import PDFFileSerializer
import io


class UploadPDFView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None, *args, **kwargs):
        serializer = PDFFileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            pdf_file = serializer.instance.file.path
            cmyk_info = self.extract_cmyk(pdf_file)
            return SuccessResponse(data={"cmyk_info": cmyk_info}).to_response()
        return ErrorResponse(data=serializer.errors).to_response()

    def extract_cmyk(self, pdf_path):
        reader = PdfReader(pdf_path)
        pages_info = []
        for page_number, page in enumerate(reader.pages):
            try:
                xObject = page['/Resources']['/XObject'].get_object()
                page_cmyk = []
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        data = xObject[obj].get_data()
                        img = Image.open(io.BytesIO(data))
                        if img.mode == "CMYK":
                            page_cmyk.append(True)
                        else:
                            page_cmyk.append(False)
                pages_info.append({"page": page_number + 1, "cmyk": any(page_cmyk)})
            except:
                pages_info.append({"page": page_number + 1, "cmyk": False})
        return pages_info
