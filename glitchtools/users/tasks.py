import datetime

from celery.task import task

from glitchtools.users.models import GlitchUser
from glitchtools.utils.api import api
from glitchtools.utils.redis import redis

@task(ignore_result=True)
def update_users():
    update_cutoff = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    login_cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    for tsid in GlitchUser.objects.filter(last_update__lt=update_cutoff, last_login__gt=login_cutoff).values_list('tsid', flat=True):
        update_user.apply_async(args=[tsid])


@task(ignore_result=True)
def update_user(tsid):
    lock = redis.lock('celery-lock-update_user-%s'%tsid, 300)
    if lock.acquire(False):
        # Good to go
        try:
            info = api.players.fullInfo(player_tsid=tsid)
            GlitchUser.objects.filter(tsid=tsid).update(last_update=datetime.datetime.utcnow(), location=info.get('location', {}).get('tsid', ''))
        finally:
            lock.release()
    else:
        return
