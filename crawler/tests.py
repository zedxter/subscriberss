#-*- coding: utf8 -*-
from django.utils import unittest
from django.db.utils import IntegrityError
from models import Article, RssUrl


class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        self.url = RssUrl.objects.create(link='http://habrahabr.ru/rss/')
        article = Article.objects.create(rss_url=self.url,
                                         guid='guid',
                                         title='title',
                                         link='link',
                                         description='description')
        
    def test_add_article(self):
        def add_unique():
            for x in range(2):
                article = Article.objects.create(rss_url=self.url,
                                                 guid='guid',
                                                 title='title',
                                                 link='link',
                                                 description='description')
        
        with self.assertRaises(IntegrityError):
            add_unique()

