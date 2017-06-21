from rest_framework.serializers import ModelSerializer

from comments.models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'user',
            'object_id',
            'content',
            'timestamp',
        ]