#-*- coding: utf8 -*-
import json
import string
import random
from django.http import HttpResponse
from django.db.utils import IntegrityError
from forms import SubscribeForm
from models import Subscribe, RssUrl

def response_json(response_dict):
    return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')
    
def random_string(n):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for _ in xrange(n)])
    
def new(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            url = form.cleaned_data['feed_link']
            try:
                rss_url = RssUrl.objects.get(link=url)
            except RssUrl.DoesNotExist:
                print 'url not found'
                rss_url = RssUrl(link=url, active=False)
                rss_url.save()
                
            token = random_string(24)
                
            subscribe = Subscribe(rss_url=rss_url,
                                  email=email,
                                  active=False,
                                  token=token)

            # TODO: письмо подписчику

            try:
                subscribe.save()
            except IntegrityError:
                return response_json({'status': 1, 'message': 'subscribe already exists'})
            
            return response_json({'status': 0, 'message': 'subscribe added'})
        
        else:
            return response_json({'status': 1, 'message': 'form is invalid', 'form_errors': form.errors})
        
    else:
        return HttpResponse(status=405)
        
def manage(request, action, subscribe_id, token):
    try:
        subscribe = Subscribe.objects.get(id=subscribe_id,
                                          token=token)
        rss_url = RssUrl.objects.get(link=subscribe.rss_url)

        if action == 'activate':
            if not subscribe.active:
                subscribe.active = True
                subscribe.save()
                return response_json({'status': 0, 'message': 'subscribe activated'})
            else:
                return response_json({'status': 1, 'message': 'subscribe already active'})

        elif action == 'deactivate':
            if subscribe.active:
                subscribe.active = False
                subscribe.save()
                return response_json({'status': 0, 'message': 'subscribe deactivated'})
            else:
                return response_json({'status': 1, 'message': 'subscribe already inactive'})

    except Subscribe.DoesNotExist:
        return HttpResponse(status=404)