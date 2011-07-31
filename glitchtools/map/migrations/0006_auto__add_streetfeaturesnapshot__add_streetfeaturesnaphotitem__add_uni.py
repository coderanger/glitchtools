# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StreetFeatureSnapshot'
        db.create_table('map_streetfeaturesnapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feature_snapshots', to=orm['map.Street'])),
            ('ts', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('map', ['StreetFeatureSnapshot'])

        # Adding model 'StreetFeatureSnaphotItem'
        db.create_table('map_streetfeaturesnaphotitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snapshot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['map.StreetFeatureSnapshot'])),
            ('feature', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('map', ['StreetFeatureSnaphotItem'])

        # Adding unique constraint on 'Street', fields ['tsid']
        db.create_unique('map_street', ['tsid'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Street', fields ['tsid']
        db.delete_unique('map_street', ['tsid'])

        # Deleting model 'StreetFeatureSnapshot'
        db.delete_table('map_streetfeaturesnapshot')

        # Deleting model 'StreetFeatureSnaphotItem'
        db.delete_table('map_streetfeaturesnaphotitem')


    models = {
        'map.hub': {
            'Meta': {'object_name': 'Hub'},
            'id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'map.street': {
            'Meta': {'object_name': 'Street'},
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connections_rel_+'", 'to': "orm['map.Street']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streets'", 'to': "orm['map.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'map.streetfeaturesnaphotitem': {
            'Meta': {'object_name': 'StreetFeatureSnaphotItem'},
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snapshot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['map.StreetFeatureSnapshot']"})
        },
        'map.streetfeaturesnapshot': {
            'Meta': {'object_name': 'StreetFeatureSnapshot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feature_snapshots'", 'to': "orm['map.Street']"}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['map']
