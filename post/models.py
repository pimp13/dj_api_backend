from django.conf import settings
from django.db import models
from django.utils.encoding import iri_to_uri
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=250, verbose_name="عنوان پست")
    content = models.TextField(verbose_name="متن محتوا")
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{slug}-{counter}"
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
            base_slug = "post"

        self.slug = self._generate_unique_slug(base_slug)
        self.slug = iri_to_uri(self.slug)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        ordering = ["title", "created_at"]
