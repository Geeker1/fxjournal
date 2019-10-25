from django.test import TestCase
from django.contrib.auth.models import User
from .models import TimeStamp, BinaryEntry, ForexEntry, Reason, Lesson
from datetime import datetime
from django.utils import timezone
# Create your tests here.


class JournalTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test', password='ledum')
        cls.stamp = TimeStamp.objects.create(
            date=datetime.utcnow().date(),
            option='forex',
            owner=cls.user
        )

    def test_timestamp_returns_actual_value(self):
        self.assertEqual(self.stamp.option, 'forex')

    def test_entry_foreignKey_relate_backto_timeStamp(self):
        timeStart = timezone.make_aware(datetime.utcnow())
        timeEnded = timezone.make_aware(datetime(year=2020, month=11, day=17))
        fx_entry = ForexEntry.objects.create(
            pair='EURUSD', stamp=self.stamp,
            timeStart=timeStart,
            timeEnded=timeEnded, rMultiple=20,
            SL=1.9029, TP=1.2344, price=1.2454
        )
        self.assertEqual(fx_entry.stamp, self.stamp)
        self.assertEqual(self.stamp.forex.all()[0], fx_entry)

    def test_entry_binaryKey_relate_backto_timeStamp(self):
        time = timezone.make_aware(datetime.utcnow())
        binary_entry = BinaryEntry.objects.create(
            pair='EURUSD', stamp=self.stamp,
            time=time, result='w',
            payout=90
        )
        self.assertEqual(binary_entry.stamp, self.stamp)
        self.assertEqual(self.stamp.binary.all()[0], binary_entry)
