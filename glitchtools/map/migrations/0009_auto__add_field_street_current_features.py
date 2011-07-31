# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Street.current_features'
        db.add_column('map_street', 'current_features', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['map.StreetFeatureSnapshot']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Street.current_features'
        db.delete_column('map_street', 'current_features_id')


    models = {
        'map.hub': {
            'Meta': {'object_name': 'Hub'},
            'id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'map.street': {
            'Meta': {'object_name': 'Street'},
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connections_rel_+'", 'to': "orm['map.Street']"}),
            'current_features': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['map.StreetFeatureSnapshot']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streets'", 'to': "orm['map.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'map.streetfeaturesnapshot': {
            'Meta': {'object_name': 'StreetFeatureSnapshot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feature_snapshots'", 'to': "orm['map.Street']"}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        'map.streetfeaturesnapshotitem': {
            'Meta': {'object_name': 'StreetFeatureSnapshotItem'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snapshot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['map.StreetFeatureSnapshot']"})
        }
    }

    complete_apps = ['map']
