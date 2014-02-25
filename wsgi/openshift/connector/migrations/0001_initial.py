# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'connector_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dummy', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'connector', ['Member'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'connector_member')


    models = {
        u'connector.member': {
            'Meta': {'object_name': 'Member'},
            'dummy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['connector']