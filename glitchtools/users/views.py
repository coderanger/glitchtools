import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import requests

from glitchtools.users.models import GlitchUser
from glitchtools.utils import json
from glitchtools.utils.db import update

def login(request):
    args = {
        'response_type': 'code',
        'scope': 'identity',
        'redirect_uri': request.build_absolute_uri(reverse('glitchtools-users-token')),
        'client_id': settings.GLITCH_API_CREDENTIALS['key'],
    }
    if 'next' in request.GET:
        args['state'] = request.GET['next']
    return HttpResponseRedirect(settings.GLITCH_API_URL+'/oauth2/authorize?'+urllib.urlencode(args))


def token(request):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])
    elif 'code' not in request.GET:
        raise Exception('No authorization code given')
    r = requests.post(settings.GLITCH_API_URL+'/oauth2/token?', {
        'grant_type': 'authorization_code',
        'code': request.GET['code'],
        'client_id': settings.GLITCH_API_CREDENTIALS['key'],
        'client_secret': settings.GLITCH_API_CREDENTIALS['secret'],
        'redirect_uri': request.build_absolute_uri(reverse('glitchtools-users-token')),
    }, timeout=2)
    if r.status_code != 200:
        raise Exception(r.content)
    token = json.loads(r.content)
    auth = request.glitch_api.auth.check(oauth_token=token['access_token'])
    scope = GlitchUser.SCOPES_MAP[token['scope']]
    try:
        glitch_user = GlitchUser.objects.get(tsid=auth['player_tsid'])
        if glitch_user.scope < scope:
            update(glitch_user, token=token['access_token'], scope=scope)
    except GlitchUser.DoesNotExist:
        # New user, create them
        user = User.objects.create_user(auth['player_name'], '', '')
        glitch_user = GlitchUser.objects.create(user=user, tsid=auth['player_tsid'], token=token['access_token'], scope=scope)
    next = request.GET.get('state', '/')
    if not next.startswith('/'):
        next = '/'
    return HttpResponseRedirect(request.build_absolute_uri(next))
