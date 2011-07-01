from crawler.models import RssUrl, Article
from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'rss_url', 'parsed_date')

class RssUrlAdmin(admin.ModelAdmin):
    list_display = ('link', 'active')

admin.site.register(RssUrl, RssUrlAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)