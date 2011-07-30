from celery.task import task

from glitchtools.map.models import Hub
from glitchtools.utils.api import api

@task
def update_hubs():
    hubs = api.locations.getHubs()
    Hub.objects.all().delete()
    for id, vals in hubs['hubs'].iteritems():
        Hub.objects.create(id=id, name=vals['name'])
