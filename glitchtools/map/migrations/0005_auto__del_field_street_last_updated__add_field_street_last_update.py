# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Street.last_updated'
        db.delete_column('map_street', 'last_updated')

        # Adding field 'Street.last_update'
        db.add_column('map_street', 'last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0)), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Street.last_updated'
        db.add_column('map_street', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0)), keep_default=False)

        # Deleting field 'Street.last_update'
        db.delete_column('map_street', 'last_update')


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
            'tsid': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['map']
