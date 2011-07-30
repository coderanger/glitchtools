from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

class GlitchUser(models.Model):
    SCOPES = [
        (1, 'identity'),
        (2, 'read'),
        (3, 'write'),
    ]
    # For reverse lookups
    SCOPES_MAP = dict((v, k) for k, v in SCOPES)
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='glitch_user')
    tsid = models.CharField(_('TSID'), max_length=20, unique=True)
    token = models.CharField(_('token'), max_length=128)
    scope = models.PositiveSmallIntegerField(_('scope'), choices=SCOPES)
