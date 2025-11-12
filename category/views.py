from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from utils.response import SuccessResponse, ErrorResponse


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data).to_response()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(
                data=serializer.data,
                message="دسته‌بندی با موفقیت ایجاد شد",
                status_code=status.HTTP_201_CREATED,
            ).to_response()
        return ErrorResponse(
            message="داده‌ها نامعتبر هستند", data=serializer.errors
        ).to_response()


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data).to_response()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(
                data=serializer.data, message="بروزرسانی با موفقیت انجام شد"
            ).to_response()
        return ErrorResponse(
            message="داده‌ها نامعتبر هستند", data=serializer.errors
        ).to_response()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message="دسته‌بندی با موفقیت حذف شد").to_response()
