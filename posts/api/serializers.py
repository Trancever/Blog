from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "publish",
            "timestamp",
        ]


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
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
