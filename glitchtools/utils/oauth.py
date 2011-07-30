from django.conf import settings
import oauth2 as oauth

consumer = oauth.Consumer(settings.GLITCH_API_CREDENTIALS['key'], settings.GLITCH_API_CREDENTIALS['secret'])
client = oauth.Client(consumer, timeout=2)
