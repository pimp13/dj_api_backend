from django.contrib import admin

from post.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'has_img')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')

    def has_img(self, obj):
        return bool(obj.image)

    has_img.boolean = True
    has_img.short_description = 'Has Img'
