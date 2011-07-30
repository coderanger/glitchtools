import urllib
import urlparse

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from glitchtools.utils import oauth

def login(request):
    body = urllib.urlencode({
        'response_type': 'code',
        'scope': 'identity',
        'redirect_uri': request.build_absolute_uri('/oauth/'),
    })
    resp, content = oauth.client.request('http://api.glitch.com/oauth2/token', body=body)
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))
    return HttpResponseRedirect("http://api.glitch.com/oauth2/authorize?oauth_token=%s"%request_token['oauth_token'])

def comingsoon(request):
    return TemplateResponse(request, 'glitchtools/core/comingsoon.html', {})
