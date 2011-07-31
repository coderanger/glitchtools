import collections
import datetime
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from glitchtools.utils.db import TSIDField, update

FEATURES_RE = re.compile(r'<b>(?:(\d*) )?([^<]+)</b>')

FEATURES = (
    'A Firefly Swarm',
    'Alchemical Goods Vendor',
    'Alph',
    'Animal Goods Vendor',
    'Bean Tree',
    'Beryl Rock for mining',
    'Bubble Tree',
    'Butterfly',
    'Chicken',
    'Cosma',
    'Crop Garden plots',
    'Dullite Rock for mining',
    'Egg Plant',
    'Friendly',
    'Fruit Tree',
    'Gardening Goods Vendor',
    'Gardening Tools Vendor',
    'Gas Plant',
    'Grendaline',
    'Groceries Vendor',
    'Hardware Vendor',
    'Humbaba',
    'Jellisac Growth',
    'Kitchen Tools Vendor',
    'Lem',
    'Mab',
    'Meal Vendor',
    'Metal Rock for mining',
    'Mining Vendor',
    'Mortar Barnacle',
    'Paper Tree',
    'Patch',
    'Peat Bog',
    'Piggy',
    'Pot',
    'Produce Vendor',
    'Sparkly Rock for mining',
    'Spice Plant',
    'Spriggan',
    'Ti',
    'Tool Vendor',
    'Wood Tree',
    'Zille',
)

FEATURES_PLURALS = {
    'Bean Trees': 'Bean Tree',
    'Beryl Rocks for mining': 'Beryl Rock for mining',
    'Bubble Trees': 'Bubble Tree',
    'Butterflies': 'Butterfly',
    'Chickens': 'Chicken',
    'Dullite Rocks for mining': 'Dullite Rock for mining',
    'Egg Plants': 'Egg Plant',
    'Fruit Trees': 'Fruit Tree',
    'Gas Plants': 'Gas Plant',
    'Jellisac Growths': 'Jellisac Growth',
    'Metal Rocks for mining': 'Metal Rock for mining',
    'Mortar Barnacles': 'Mortar Barnacle',
    'Paper Trees': 'Paper Tree',
    'Patches': 'Patch',
    'Peat Bogs': 'Peat Bog',
    'Piggies': 'Piggy',
    'Sparkly Rocks for mining': 'Sparkly Rock for mining',
    'Spice Plants': 'Spice Plant',
    'Wood Trees': 'Wood Tree',
}

class Hub(models.Model):
    """Data model for a single Glitch hub (called a region in-game)."""
    id = models.PositiveSmallIntegerField(_('id'), primary_key=True)
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name


class Street(models.Model):
    """Data model for a single Glitch street."""
    hub = models.ForeignKey(Hub, verbose_name=_('hub'), related_name='streets')
    tsid = TSIDField(_('tsid'), unique=True)
    name = models.CharField(_('name'), max_length=100)
    deleted = models.BooleanField(_('deleted'), default=False)
    last_update = models.DateTimeField(_('last update'), default=datetime.datetime.utcfromtimestamp(0))
    connections = models.ManyToManyField('self', verbose_name=_('connections'))
    current_features = models.ForeignKey('StreetFeatureSnapshot', null=True, verbose_name=_('current features'), related_name='+')

    def __unicode__(self):
        return self.name

    def search(self, search_fn):
        if search_fn(self):
            return (self.id,)
        explored = set()
        unexplored = collections.deque((id, (self.id,)) for id in self.connections.values_list('id', flat=True))
        while unexplored:
            cur_id, cur_path = unexplored.popleft()
            cur = Street.objects.select_related('current_features').get(id=cur_id)
            new_path = cur_path + (cur_id,)
            if search_fn(cur):
                return new_path
            explored.add(cur.id)
            unexplored.extend((id, new_path) for id in cur.connections.values_list('id', flat=True) if id not in explored)

    def set_features(self, raw_features):
        # Clean up the raw features strings, normalize to lowercase, and de-pluralize
        features = {}
        for count, feature in FEATURES_RE.findall(''.join(raw_features)):
            features[FEATURES_PLURALS.get(feature, feature).lower()] = int(count or 0)
        if not self.current_features or not self.current_features.features_equal(features):
            snapshot = StreetFeatureSnapshot.objects.create(street=self)
            for feature, count in features.iteritems():
                StreetFeatureSnapshotItem.objects.create(snapshot=snapshot, feature=feature, count=count)
            update(self, current_features=snapshot)


class StreetFeatureSnapshot(models.Model):
    """Data model for a snapshot in time of the features on a street."""
    street = models.ForeignKey(Street, verbose_name=_('street'), related_name='feature_snapshots')
    ts = models.DateTimeField(_('timestamp'), default=datetime.datetime.utcnow)

    def features_equal(self, features):
        """Is the given dict of {'feature': count} the same as this snapshot."""
        items = self.items.all()
        if len(items) != len(features):
            return False
        for it in items:
            if features.get(it.feature) != it.count:
                return False
        return True


class StreetFeatureSnapshotItem(models.Model):
    """Data model for a single feature on a street."""
    snapshot = models.ForeignKey(StreetFeatureSnapshot, verbose_name=_('snapshot'), related_name='items')
    feature = models.CharField(_('feature'), max_length=100, choices=((s.lower(),s) for s in FEATURES))
    count = models.IntegerField(_('count'), default=1)
