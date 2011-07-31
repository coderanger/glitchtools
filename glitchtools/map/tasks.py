import datetime

from celery.task import task

from glitchtools.map.models import Hub, Street
from glitchtools.utils.api import api
from glitchtools.utils.db import update

@task(ignore_result=True)
def update_hubs():
    hubs = api.locations.getHubs()
    Hub.objects.all().delete()
    for id, vals in hubs['hubs'].iteritems():
        Hub.objects.create(id=id, name=vals['name'])


@task(ignore_result=True)
def update_streets():
    for id in Hub.objects.all().values_list('id', flat=True):
        update_street.apply_async(args=[id])


@task(ignore_result=True)
def update_street(hub_id):
    streets = api.locations.getStreets(hub_id=hub_id)
    seen_ids = set()
    for tsid, vals in streets['streets'].iteritems():
        seen_ids.add(tsid)
        Street.objects.get_or_create(hub_id=hub_id, tsid=tsid, defaults={'name': vals['name']})
    # Block any we didn't see
    Street.objects.filter(hub=hub_id).exclude(tsid__in=seen_ids).update(deleted=True)


@task(ignore_result=True)
def update_streets_info(force=False):
    update_cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    if force:
        qs = Street.objects.all()
    else:
        qs = Street.objects.filter(last_update__lt=update_cutoff)
    for tsid in qs.filter(deleted=False).values_list('tsid', flat=True):
        update_street_info.apply_async(args=[tsid])


@task(ignore_result=True)
def update_street_info(tsid):
    info = api.locations.streetInfo(street_tsid=tsid)
    street = Street.objects.get(tsid=tsid)
    street.connections.exclude(tsid__in=info['connections']).delete()
    for connection_tsid in info['connections'].iterkeys():
        try:
            connection_street = Street.objects.get(tsid=connection_tsid)
        except Street.DoesNotExist:
            vals = info['connections'][connection_tsid]
            connection_street = Street.objects.create(hub_id=vals['hub']['id'], tsid=connection_tsid, name=vals['name'])
        street.connections.add(connection_street)
    update(street, last_update=datetime.datetime.utcnow())
