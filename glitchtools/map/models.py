import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from glitchtools.utils.db import TSIDField

class Hub(models.Model):
    id = models.PositiveSmallIntegerField(_('id'), primary_key=True)
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name


class Street(models.Model):
    hub = models.ForeignKey(Hub, verbose_name=_('hub'), related_name='streets')
    tsid = TSIDField(_('tsid'))
    name = models.CharField(_('name'), max_length=100)
    deleted = models.BooleanField(_('deleted'), default=False)
    last_update = models.DateTimeField(_('last update'), default=datetime.datetime.utcfromtimestamp(0))
    connections = models.ManyToManyField('self', verbose_name=_('connections'))

    def __unicode__(self):
        return self.name
