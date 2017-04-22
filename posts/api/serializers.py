from rest_framework.serializers import ModelSerializer

from posts.models import Post

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "slug",
            "image",
            "content",
            "height_field",
            "width_field",
            "draft",
            "publish",
            "timestamp",
        ]