from django.db import models
from django.utils.encoding import iri_to_uri
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(
        max_length=190, verbose_name="عنوان دسته بندی", db_index=True
    )
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    is_active = models.BooleanField(
        default=True, verbose_name="فعال است؟", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
        else:
            base_slug = slugify(self.slug, allow_unicode=True)

        if not base_slug:
            base_slug = "category"

        self.slug = self._generate_unique_slug(base_slug)
        self.slug = iri_to_uri(self.slug)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["title"]
