from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from subscribe.models import Article, RssUrl
import feedparser


class Command(BaseCommand):
    def handle(self, *args, **optionals):
        for url in RssUrl.objects.filter(active=True):
            feed = feedparser.parse(url.link)
            items = feed.get('items')
            if not items:
                continue

            for item in feed["items"]:
                article = Article(rss_url=url)
                
                guid = item.get('guid')
                if guid:
                    article.guid = item.get('guid')
                else:
                    article.guid = item.get('title')
                    
                article.title = item.get('title')
                article.link = item.get('link')
                article.description = item.get('description')
                
                try:
                    article.save()
                except IntegrityError:
                    continue
