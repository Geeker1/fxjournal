from django.db import models
import uuid
from django.conf import settings

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


class BaseManager(models.Manager):
    arguments = ('r_text', 'l_text', 'r_image', 'l_image')

    def create_entry(self, **kwargs):
        r_text, l_text, r_image, l_image = [
            kwargs.pop(val) for val in self.arguments]

        entry = self.model.objects.create(**kwargs)
        Reason.objects.create(image=r_image, text=r_text, entry=entry)
        Lesson.objects.create(image=l_image, text=l_text, entry=entry)
        return entry


class BaseEntry(models.Model):
    entry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    CHOICE = (('b', 'Buy'), ('s', 'Sell'))
    pair = models.CharField(max_length=7, )
    option = models.CharField(choices=CHOICE, max_length=1, default='b')
    objects = BaseManager()

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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='user_directory_path', blank=True, null=True)
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
