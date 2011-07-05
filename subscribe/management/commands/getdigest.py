from django.core.management.base import BaseCommand
from subscribe.models import Rss, Article, MailTask
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from subscribe.views import manage
import settings
import re


class Command(BaseCommand):
    
    def handle(self, *args, **optionals):

        rss_q = Rss.objects.filter(subscription__active=True)
        rss_q.query.group_by = ['rss_id']
        
        for rss in rss_q:

            rss_subscr = rss.subscription.filter(active=True)

            if rss_subscr:
                digest_articles = Article.objects.filter(id__gt=rss.last_sent_id, rss=rss)

                if digest_articles:
                    for subscr in rss_subscr:
                        unsubscribe_url = '%s%s' % (re.sub(r'/$', '', settings.SERVICE_EXTERNAL_ROOT_URL),
                                                    reverse(manage, args=['deactivate', subscr.id, subscr.token]))
                        message = render_to_string('digest.html', locals())

                        m_task = MailTask(subscribe=subscr,
                                          rss=rss,
                                          title=rss.title,
                                          message=message)
                        m_task.save()


                    rss.last_sent_id = max([a.id for a in digest_articles])
                    rss.save()
