from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from subscribe.models import Article, Rss, Subscription
import feedparser


class Command(BaseCommand):

    def handle(self, *args, **optionals):

        for rss in Rss.objects.filter(subscription__active=True):
            feed = feedparser.parse(rss.link)

            if not rss.title:
                rss.title = feed['channel'].get('title')
                rss.save()

            items = feed.get('items')
            if not items:
                continue

            for item in feed["items"]:
                article = Article(rss=rss)

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
