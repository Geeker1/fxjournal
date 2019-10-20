from django.db import models
import uuid
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.


class TimeStamp(models.Model):
    CHOICE = (('forex', 'forex'), ('binary', 'binary'))

    date = models.DateField()
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    option = models.CharField(choices=CHOICE, max_length=10, blank=True)

    def __str__(self):
        return f"Timestamp for {self.date}"

    class Meta:
        ordering = ['-date']


class BaseEntry(models.Model):
    entry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    CHOICE = (('b', 'Buy'), ('s', 'Sell'))
    pair = models.CharField(max_length=7, )
    option = models.CharField(choices=CHOICE, max_length=1, default='b')

    def __str__(self):
        return f"Entry for {self.pair} @ {self.stamp.date}"


class ForexEntry(BaseEntry):
    timeStart = models.DateTimeField()
    timeEnded = models.DateTimeField()
    rMultiple = models.IntegerField()
    SL = models.FloatField()
    price = models.FloatField()
    TP = models.FloatField()
    stamp = models.ForeignKey(
        TimeStamp, on_delete=models.CASCADE,
        related_name='forex'
    )


class BinaryEntry(BaseEntry):

    CHOICE = (
        ('w', 'Win'),
        ('l', 'Lose'),
    )
    payout = models.IntegerField()
    result = models.CharField(choices=CHOICE, max_length=1)
    time = models.TimeField()
    stamp = models.ForeignKey(
        TimeStamp, on_delete=models.CASCADE,
        related_name='binary'
    )


class ContentBase(models.Model):

    def user_directory_path(self):
        return 'user_{0}/contents'.format(self.owner.username)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    text = models.TextField()

    class Meta:
        abstract = True


class Reason(ContentBase):
    entry = models.OneToOneField(
        'BaseEntry',
        on_delete=models.CASCADE,
        related_name='reason'
    )


class Lesson(ContentBase):
    entry = models.OneToOneField(
        'BaseEntry',
        on_delete=models.CASCADE,
        related_name='lesson'
    )


# class Content(models.Model):
#     content_type = models.ForeignKey(
#         ContentType,
#         limit_choices_to={
#             'model__in': ('image', 'text')
#         },
#         on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):
#         return self.tag


# class ItemBase(models.Model):
#     title = models.CharField(max_length=10)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def user_directory_path(self, instance):
#         # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#         return 'user_{0}/contents'.format(instance.owner.username)

#     class Meta:
#         abstract = True


# class Image(ItemBase):
#     image = models.ImageField(upload_to=ItemBase.user_directory_path)
#     external_link = models.URLField()


# class Text(ItemBase):
#     text = models.TextField()

