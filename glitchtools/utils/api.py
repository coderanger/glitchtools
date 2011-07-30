from django.conf import settings
import requests

from glitchtools.utils import json

class GlitchAPIError(Exception):
    """An error in a Glitch API method."""


class ServiceProxy(object):
    def __init__(self, service_url, service_name=None, token=None, timeout=10):
        self._service_url = service_url
        self._service_name = service_name
        self._token = token
        self._timeout = timeout

    def __getattr__(self, name):
        if self._service_name != None:
            name = '%s.%s' % (self._service_name, name)
        return self.__class__(self._service_url, name, token=self._token, timeout=self._timeout)

    def __repr__(self):
        return '<%s %s>'%(self.__class__.name, self._service_name)

    def __call__(self, **kwargs):
        if 'oauth_token' not in kwargs and self._token:
            kwargs['oauth_token'] = self._token
        timeout = kwargs.pop('timeout', None) or self._timeout
        resp_data = self._request(self._service_url + '/simple/' + self._service_name, kwargs, timeout)
        try:
            resp = json.loads(resp_data)
        except Exception, e:
            raise GlitchAPIError(str(e))
        else:
            if resp.get('ok'):
                return resp
            else:
                GlitchAPIError(resp.get('error', 'Unknown error'))

    def _request(self, url, params, timeout):
        req = requests.get(url, params, timeout=timeout)
        return req.content


api = ServiceProxy(settings.GLITCH_API_URL)
