from django.core.management.base import BaseCommand
from subscribe.models import Rss, Article, Subscription, MailTask
from django.core.urlresolvers import reverse
from subscribe.views import manage


class Command(BaseCommand):
    
    def handle(self, *args, **optionals):

        subscriptions = Subscription.objects.filter(active=True)

        for rss in Rss.objects.all():
            this_rss_subscr = subscriptions.filter(rss=rss)

            if this_rss_subscr:
                digest_articles = Article.objects.filter(id__gt=rss.last_sent_id, rss=rss)

                if digest_articles:
                    digest_mail_body = '<br><br>'.join('<a href="%s">%s</a><br>%s' % (a.link, a.title, a.description) for a in digest_articles)

                    for subscr in this_rss_subscr:
                        unsubscribe_url = reverse(manage, args=['deactivate', subscr.id, subscr.token])
                        m_task = MailTask(subscribe=subscr,
                                          rss=rss,
                                          title=rss.title,
                                          message='%s<br><br><br>%s' % (digest_mail_body, unsubscribe_url))
                        m_task.save()


                    rss.last_sent_id = max([a.id for a in digest_articles])
                    rss.save()