#-*- coding: UTF-8 -*-
import json
import string
import random
import re
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.core.urlresolvers import reverse
from forms import SubscribeForm
from models import Subscription, Rss, MailTask
import settings

def response_json(response_dict):
    return HttpResponse(json.dumps(response_dict), mimetype='application/javascript')
    
def random_string(n):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for _ in xrange(n)])
    
def new(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    else:
        form = SubscribeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            url = form.cleaned_data['feed_link']
            try:
                rss_url = Rss.objects.get(link=url)
            except Rss.DoesNotExist:
                rss_url = Rss(link=url)
                rss_url.save()
                
            token = random_string(24)
                
            subscribe = Subscription(rss=rss_url,
                                  email=email,
                                  active=False,
                                  token=token)

            try:
                subscribe.save()
            except IntegrityError:
                return response_json({'status': 1, 'message': 'subscribe already exists'})

            #письмо активации подписчику
            params = {'email': email.encode('utf8'),
                      'rss': url.encode('utf8'),
                      'activate_link': '%s%s' % (re.sub(r'/$', '', settings.SERVICE_EXTERNAL_ROOT_URL),
                                                 reverse(manage, args=['activate', subscribe.id, subscribe.token]))}

            m_task = MailTask(subscribe=subscribe,
                              rss=rss_url,
                              title=settings.MAIL_ACTIVATE_TITLE,
                              message=settings.MAIL_ACTIVATE_TEMPLATE % params)
            m_task.save()

            return response_json({'status': 0, 'message': 'subscribe added'})
        
        else:
            return response_json({'status': 1, 'message': 'form is invalid', 'form_errors': form.errors})


def manage(request, action, subscribe_id, token):
    try:
        subscribe = Subscription.objects.get(id=subscribe_id,
                                          token=token)

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

    except Subscription.DoesNotExist:
        return HttpResponse(status=404)
