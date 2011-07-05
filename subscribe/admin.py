from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from models import *

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'rss', 'active')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'rss', 'parsed_date')

class RssUrlAdmin(admin.ModelAdmin):
    list_display = ('link', 'last_sent_id')

class MailTaskAdmin(admin.ModelAdmin):
    list_display = ('subscribe', 'title')

admin.site.register(Rss, RssUrlAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Subscription, SubscribeAdmin)
admin.site.register(MailTask, MailTaskAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)