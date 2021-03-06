from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, pre_delete
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

from markdown_deux import markdown
from taggit.managers import TaggableManager

from comments.models import Comment

# Dont know this
from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib
#

from django.templatetags.static import static # for access to static files

# Create your models here.


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" %(instance, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        return mark_safe(markdown(self.content))

    @property
    def comments(self):
        instance = self
        queryset = Comment.objects.filter_by_instance(self)
        return queryset

    @property
    def get_content_type(self):
        instance = self
        type = ContentType.objects.get_for_model(instance.__class__)
        return type

    class Meta:
        ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    """Create slug if instance's slug was empty"""
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)


def pre_delete_post_receiver(sender, instance, *args, **kwargs):
    """Delete tags assigned to deleted post if no other posts have this tags assigned"""
    instance_tags = instance.tags.all()
    for tag in instance_tags:
        post_objects = Post.objects.exclude(id=instance.id)
        flag = False
        for post in post_objects:
            if tag.name in post.tags.all():
                flag = True
        if flag == False:
            tag.delete()


pre_delete.connect(receiver=pre_delete_post_receiver, sender=Post)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=100&height=100".format(fb_uid[0].uid)

        return static('img/user.png')


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
