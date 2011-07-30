from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hub(models.Model):
    id = models.PositiveSmallIntegerField(_('id'), primary_key=True)
    name = models.CharField(_('name'), max_length=100)


