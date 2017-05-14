from django.test import TestCase
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from random import randint

from .models import Comment
from posts.models import Post

# Create your tests here.

class CommentManagerTestClass(TestCase):

    def test_comment_manager_all(self):
        amount = randint(0,9)
        for x in range(amount):
            Comment.objects.create(object_id=amount, content_type_id=amount)

        self.assertEquals(Comment.objects.all().count(), amount)

    def test_comment_manager_filter_by_instance(self):
        post = Post.objects.create(publish=timezone.now().date())
        amount = randint(0,9)
        for x in range(amount):
            Comment.objects.create(object_id=post.id, content_type=ContentType.objects.get_for_model(post.__class__))

        for x in range(amount):
            Comment.objects.create(object_id=100000, content_type_id=10000)

        self.assertEquals(Comment.objects.filter_by_instance(post).count(), amount)
        self.assertEquals(Comment.objects.all().count(), amount * 2)

    def test_comment_children(self):
        amount = randint(0,9)
        parent = Comment.objects.create(object_id=1, content_type=ContentType.objects.get_for_model(Post))
        for x in range(amount):
            Comment.objects.create(object_id=x, content_type=ContentType.objects.get_for_model(Post), parent=parent)

        self.assertEquals(parent.children.count(), amount)
        self.assertEquals(parent.children.order_by("object_id").first().object_id, 0)