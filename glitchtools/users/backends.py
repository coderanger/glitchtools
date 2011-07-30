from django.contrib.auth.models import User

from glitchtools.users.models import GlitchUser

class GlitchBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, tsid=None, token=None, scope=None):
        try:
            return User.objects.select_related('glitch_user').get(glitch_user__tsid=tsid)
        except User.DoesNotExist:
            user = User.objects.create_user(username, '', '')
            user.glitch_user = GlitchUser.objects.create(user=user, tsid=tsid, token=token, scope=scope)
            return user

    def get_user(self, user_id):
        try:
            return User.objects.select_related('glitch_user').get(pk=user_id)
        except User.DoesNotExist:
            return None
