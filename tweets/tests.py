from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from testing.testcases import TestCase
from tweets.constants import TweetPhotoStatus
from tweets.models import Tweet, TweetPhoto
from utils.time_helpers import utc_now


# Create your tests here.
class TweetTests(TestCase):
    def setUp(self):
        self.clear_cache()
        self.linghu = self.create_user('lingu')
        self.tweet = self.create_tweet(self.linghu, content='Jiuzhang DafaHao')

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()

        self.assertEqual(self.tweet.hours_to_now, 10)

    def test_like_set(self):
        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        dongxie = self.create_user('dongxie')
        self.create_like(dongxie, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)

    def test_create_photo(self):
        # 测试可以成功创建photo的数据对象
        photo = TweetPhoto.objects.create(
            tweet=self.tweet,
            user=self.linghu,
        )

        self.assertEqual(photo.user, self.linghu)
        self.assertEqual(photo.status, TweetPhotoStatus.PENDING)
        self.assertEqual(self.tweet.tweetphoto_set.count(), 1)