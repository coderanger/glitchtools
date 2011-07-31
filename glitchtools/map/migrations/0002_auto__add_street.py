# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Street'
        db.create_table('map_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(related_name='streets', to=orm['map.Hub'])),
            ('tsid', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('map', ['Street'])

        # Adding M2M table for field connections on 'Street'
        db.create_table('map_street_connections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_street', models.ForeignKey(orm['map.street'], null=False)),
            ('to_street', models.ForeignKey(orm['map.street'], null=False))
        ))
        db.create_unique('map_street_connections', ['from_street_id', 'to_street_id'])


    def backwards(self, orm):
        
        # Deleting model 'Street'
        db.delete_table('map_street')

        # Removing M2M table for field connections on 'Street'
        db.delete_table('map_street_connections')


    models = {
        'map.hub': {
            'Meta': {'object_name': 'Hub'},
            'id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'map.street': {
            'Meta': {'object_name': 'Street'},
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connections_rel_+'", 'to': "orm['map.Street']"}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'streets'", 'to': "orm['map.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tsid': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['map']
