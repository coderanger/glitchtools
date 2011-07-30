class GlitchUserMiddleware(object):
    def process_request(self, request):
        request.__class__.glitch_user = property(lambda self: self.user.glitch_user if self.user else None)
