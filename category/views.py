from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer
from utils.response import SuccessResponse, ErrorResponse


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت Category
    شامل CRUD و قابلیت فعال/غیرفعال کردن دسته‌بندی
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # فقط کاربران لاگین شده اجازه تغییر دارند

    def list(self, request, *args, **kwargs):
        """
        لیست همه دسته‌بندی‌ها
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data).to_response()

    def retrieve(self, request, *args, **kwargs):
        """
        نمایش یک دسته‌بندی خاص
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data).to_response()

    def create(self, request, *args, **kwargs):
        """
        ایجاد دسته‌بندی جدید
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(
                data=serializer.data,
                message="دسته‌بندی با موفقیت ایجاد شد",
                status=status.HTTP_201_CREATED,
            ).to_response()
        return ErrorResponse(
            message="داده‌ها نامعتبر هستند", data=serializer.errors
        ).to_response()

    def update(self, request, *args, **kwargs):
        """
        بروزرسانی دسته‌بندی
        """
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
        """
        حذف دسته‌بندی
        """
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message="دسته‌بندی با موفقیت حذف شد").to_response()

    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        """
        فعال/غیرفعال کردن دسته‌بندی
        """
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        status_text = "فعال شد" if instance.is_active else "غیرفعال شد"
        return SuccessResponse(
            data={"is_active": instance.is_active}, message=f"دسته‌بندی {status_text}"
        ).to_response()
