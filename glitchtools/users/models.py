import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

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
    last_update = models.DateTimeField(_('last update'), default=datetime.datetime.utcfromtimestamp(0))
    location = TSIDField(_('location'), default='')
