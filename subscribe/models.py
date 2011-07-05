#-*- coding: UTF-8 -*-
from django.db import models


class Rss(models.Model):
    link = models.URLField(unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    last_sent_id = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.link


class Article(models.Model):
    rss = models.ForeignKey(Rss, related_name='articles')
    guid = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField()
    parsed_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('rss', 'guid')


class Subscription(models.Model):
    rss = models.ForeignKey(Rss, related_name='subscription')
    email = models.EmailField()
    token = models.CharField(max_length=50)
    active = models.BooleanField()

    def __unicode__(self):
        return '%s: %s' % (self.email, self.rss)
        
    class Meta:
        unique_together = ('email', 'rss')

class MailTask(models.Model):
    STATUS_IN_PROGRESS = '0'
    STATUS_OK = '1'
    STATUS_INNER_FAILURE = '2'
    STATUS_PROVIDER_FAILURE = '3'

    STATUS_CHOICES = (
            (STATUS_IN_PROGRESS, 'IN PROGRESS'),
            (STATUS_OK, 'OK'),
            (STATUS_INNER_FAILURE, 'INNER FAILURE'),
            (STATUS_PROVIDER_FAILURE, 'PROVIDER FAILURE'),
        )

    subscribe = models.ForeignKey(Subscription)
    rss = models.ForeignKey(Rss)
    title = models.CharField(max_length=200)
    message = models.TextField()
    sent = models.CharField(choices=STATUS_CHOICES,
                            default=STATUS_IN_PROGRESS,
                            max_length=2)
    exception_message = models.TextField()
    
    def __unicode__(self):
        return self.title
