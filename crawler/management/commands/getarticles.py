from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from crawler.models import Article, RssUrl
import feedparser


class Command(BaseCommand):
    
    def handle(self, *args, **optionals):
        for url in RssUrl.objects.all():
            
            feed = feedparser.parse(url.link)
            items = feed.get('items')
            if not items:
                continue

            for item in feed["items"]:
                article = Article(rss_url=url)
                article.guid = item.get('guid')
                article.title = item.get('title')
                article.link = item.get('link')
                article.description = item.get('description')
                
                try:
                    article.save()
                except IntegrityError:
                    continue