from django.core.management.base import BaseCommand
from subscribe.models import Rss, Article, Subscription, MailTask
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from subscribe.views import manage


class Command(BaseCommand):
    
    def handle(self, *args, **optionals):

        for rss in Rss.objects.filter(subscription__active=True):
            this_rss_subscr = Subscription.objects.filter(rss=rss)

            if this_rss_subscr:
                digest_articles = Article.objects.filter(id__gt=rss.last_sent_id, rss=rss)

                if digest_articles:
                    for subscr in this_rss_subscr:
                        unsubscribe_url = reverse(manage, args=['deactivate', subscr.id, subscr.token])
                        message = render_to_string('digest.html', locals())
                        
                        m_task = MailTask(subscribe=subscr,
                                          rss=rss,
                                          title=rss.title,
                                          message=message)
                        m_task.save()


                    rss.last_sent_id = max([a.id for a in digest_articles])
                    rss.save()