from django.db import models

class RssUrl(models.Model):
    link = models.URLField()
    
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