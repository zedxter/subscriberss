#-*- coding: utf8 -*-
from django.utils import unittest
from django.db.utils import IntegrityError
from models import Article, RssUrl


class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        self.url = RssUrl.objects.create(link='http://ololo.ru/rss/')

    def tearDown(self):
        self.url.delete()

        
    def test_add_article_unique_link_guid(self):
        def _helper():
            for _ in range(2):
                Article.objects.create(rss_url=self.url,
                                       guid='guid',
                                       title='title',
                                       link='link',
                                       description='description')

        self.assertRaises(IntegrityError, _helper)
