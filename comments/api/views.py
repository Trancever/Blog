from rest_framework.generics import ListAPIView

from comments.models import Comment
from .serializers import CommentSerializer

class CommentsListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer