from django.test import TestCase
from django.utils import timezone

from .models import (upload_location, Post, PostManager)

# Create your tests here.


class UploadLocationTest(TestCase):

    def test_upload_location_posittive_case(self):
        instance = Post(title="title")
        filename = "file"

        self.assertEquals("title/file", upload_location(instance, filename))

    def test_upload_location_negative_case(self):
        title = "some words here"
        slug = "some-words-here"
        instance = Post(title=title, slug=title)
        filename = "filename"

        self.assertEquals(title, upload_location(instance, filename).split("/")[0])
        self.assertNotEqual(slug + "/" + filename, upload_location(instance, filename))


class PostManagerTest(TestCase):

    def test_post_manager_active(self):
        post1 = Post(title="title1", draft=True, publish=timezone.now())
        post2 = Post(title="title2", draft=False, publish=timezone.now())
        post3 = Post(title="title3", draft=True, publish=timezone.now() + timezone.timedelta(days=10))

        post1.save()
        post2.save()
        post3.save()

        self.assertEquals(Post.objects.active().count(), 1)


class PreSavePostReceiverTest(TestCase):

    def test_pre_save_post_receiver(self):
        title = "4 words in title"
        slug = "4-words-in-title"
        post = Post(title=title, publish=timezone.now())
        post.save()
        qs = Post.objects.all().filter(title=title)
        self.assertEquals(len(qs), 1)
        self.assertEquals(qs.first().slug, slug)