from django.conf import settings

from glitchtools.utils.api import ServiceProxy

class GlitchUserMiddleware(object):
    def process_request(self, request):
        request.__class__.glitch_user = property(lambda self: self.user.glitch_user if self.user.is_authenticated() else None)
        request.__class__.glitch_api = property(lambda self: ServiceProxy(settings.GLITCH_API_URL, token=(self.glitch_user.token if self.glitch_user else None), timeout=2))
