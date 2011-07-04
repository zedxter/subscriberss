#-*- coding: utf8 -*-
import json
from django.test.client import Client
from django.utils import unittest
from django.db.utils import IntegrityError
from models import Article, Rss
from subscribe.models import Subscription


class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        self.rss = Rss.objects.create(link='http://example.com/rss/')


    def tearDown(self):
        self.rss.delete()
        Article.objects.all().delete()


    def test_add_article_unique_link_guid(self):
        def _helper():
            for _ in xrange(2):
                Article.objects.create(rss=self.rss,
                                       guid='guid',
                                       title='title',
                                       link='link',
                                       description='description')

        self.assertRaises(IntegrityError, _helper)


class ActivateDeactivateSubscriptionTestCase(unittest.TestCase):
    def setUp(self):
        self.rss = Rss.objects.create(link='http://example.com/rss/')
        inactive_subscription_token = '1'
        self.subscr = Subscription.objects.create(rss=self.rss, email='email1@example.com',
                                                              token=inactive_subscription_token,
                                                              active=False)
        self.client = Client()


    def tearDown(self):
        self.rss.delete()
        self.subscr.delete()


    def test_activate_non_existing_404(self):
        resp = self.client.post('/subscribe/activate/9000/invalidtoken/', {})
        self.assertEqual(resp.status_code, 404)

    def test_activate_deactivate_ok(self):
        def _helper(is_active):
            if not is_active:
                action = 'activate'
            else:
                action = 'deactivate'

            url_activate = '/subscribe/%s/%s/%s/' % (action,
                                                     self.subscr.id,
                                                     self.subscr.token,)
            resp = self.client.post(url_activate)
            self.assertEqual(resp.status_code, 200)

            json_resp = json.loads(resp.content)
            self.assertEqual(json_resp['status'], 0)

            self.subscr = Subscription.objects.get(pk=self.subscr.id)
            self.assertEqual(not is_active, self.subscr.active)

        _helper(False)
        _helper(True)


class NewSubscribeTestCase(unittest.TestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.feed_link = 'http://example.com/rss/'
        self.client = Client()
        
    def tearDown(self):
        self.rss.delete()
        self.subscr.delete()
    
    def test_add_new_ok(self):
        subscr_count = Subscription.objects.all().count()
        self.assertEqual(subscr_count, 0)
        
        req = lambda: self.client.post('/subscribe/new/', {'feed_link': self.feed_link, 'email': self.email})
        
        resp = req()
        self.assertEqual(resp.status_code, 200)
        
        self.rss = Rss.objects.get(link=self.feed_link)
        self.subscr = Subscription.objects.get(email=self.email)
        
        resp2 = req()
        json_resp = json.loads(resp2.content)
        self.assertEqual(json_resp['status'], 1)
        
        