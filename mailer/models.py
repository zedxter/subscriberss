from django.db import models
from subscribe.models import Subscribe
from crawler.models import Article

class MailTask(models.Model):
    subscribe = models.ForeignKey(Subscribe)
    articles = models.ManyToManyField(Article)
    sent = models.BooleanField()
    
    def __unicode__(self):
        return self.subscribe