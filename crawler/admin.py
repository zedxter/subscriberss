from crawler.models import RssUrl, Article
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'rss_url', 'parsed_date')

admin.site.register(RssUrl)
admin.site.register(Article, ArticleAdmin)