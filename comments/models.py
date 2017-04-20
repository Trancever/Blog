from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.db import models


class CommentManager(models.Manager):
    def all(self):
        queryset = super(CommentManager, self).filter(parent=None)
        return queryset

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        queryset = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return queryset


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)

    @property
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def save(self, *args, **kwargs):
        self.updated = timezone.now().date()
        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-timestamp"]