from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "updated", "timestamp"]
    list_filter = ["title", "timestamp", "updated"]
    search_fields = ["title"]
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)