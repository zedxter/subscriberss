from django.db import models


class RssUrl(models.Model):
    link = models.URLField(unique=True)
    active = models.BooleanField()
    
    def __unicode__(self):
        return self.link
    

class Article(models.Model):
    rss_url = models.ForeignKey(RssUrl)
    guid = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField()
    parsed_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        unique_together = ('rss_url', 'guid')


class Subscribe(models.Model):
    rss_url = models.ForeignKey(RssUrl)
    email = models.EmailField()
    token = models.CharField(max_length=50)
    active = models.BooleanField()
    last_sent = models.ForeignKey(Article, blank=True, null=True)
    
    def __unicode__(self):
        return '%s: %s' % (self.email, self.rss_url)
        
    class Meta:
        unique_together = ('email', 'rss_url')


class MailTask(models.Model):
    subscribe = models.ForeignKey(Subscribe)
    articles = models.ManyToManyField(Article)
    sent = models.BooleanField()
    
    def __unicode__(self):
        return self.subscribe
