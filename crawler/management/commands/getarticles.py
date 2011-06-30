from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from crawler.models import Article, RssUrl
import feedparser
from datetime import datetime


class Command(BaseCommand):
    
    def handle(self, *args, **optionals):
        for url in RssUrl.objects.all():
            
            feed = feedparser.parse(url.link)
            items = getattr(feed, 'items')
            if not items:
                continue

            for item in feed["items"]:
                article = Article(rss_url_id=url.id)
                article.guid = item.get('guid')
                article.title = item.get('title')
                article.link = item.get('link')
                article.description = item.get('description')
                date_parsed = datetime.now()
                article.parsed = date_parsed.strftime('%Y-%m-%d %H:%M:%S')
                
                try:
                    article.save()
                except IntegrityError:
                    continue