import datetime

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.utils.translation import ugettext_lazy as _

from glitchtools.utils.db import TSIDField

class GlitchUser(models.Model):
    SCOPES = [
        (1, 'identity'),
        (2, 'read'),
        (3, 'write'),
    ]
    # For reverse lookups
    SCOPES_MAP = dict((v, k) for k, v in SCOPES)
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='glitch_user')
    tsid = TSIDField(_('TSID'), unique=True)
    token = models.CharField(_('token'), max_length=128)
    scope = models.PositiveSmallIntegerField(_('scope'), choices=SCOPES)
    last_login = models.DateTimeField(_('last login'), default=datetime.datetime.utcnow) # auth.User stores this in local timezone, fail
    last_update = models.DateTimeField(_('last update'), default=datetime.datetime.utcfromtimestamp(0))
    location = TSIDField(_('location'), default='', blank=True)

    def __unicode__(self):
        return self.tsid


def update_last_login(sender, user, **kwargs):
    now = datetime.datetime.utcnow()
    if hasattr(user, '_glitch_user_cache'):
        user.glitch_user.last_login = now
    GlitchUser.objects.filter(user=user.id).update(last_login=now)
user_logged_in.connect(update_last_login)
