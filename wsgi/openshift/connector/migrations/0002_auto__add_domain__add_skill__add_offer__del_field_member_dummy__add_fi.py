# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table(u'connector_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'connector', ['Domain'])

        # Adding model 'Skill'
        db.create_table(u'connector_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['connector.Member'])),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'connector', ['Skill'])

        # Adding model 'Offer'
        db.create_table(u'connector_offer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'connector', ['Offer'])

        # Deleting field 'Member.dummy'
        db.delete_column(u'connector_member', 'dummy')

        # Adding field 'Member.domain'
        db.add_column(u'connector_member', 'domain',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['connector.Domain']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Domain'
        db.delete_table(u'connector_domain')

        # Deleting model 'Skill'
        db.delete_table(u'connector_skill')

        # Deleting model 'Offer'
        db.delete_table(u'connector_offer')

        # Adding field 'Member.dummy'
        db.add_column(u'connector_member', 'dummy',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Deleting field 'Member.domain'
        db.delete_column(u'connector_member', 'domain_id')


    models = {
        u'connector.domain': {
            'Meta': {'object_name': 'Domain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'connector.member': {
            'Meta': {'object_name': 'Member'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['connector.Domain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'connector.offer': {
            'Meta': {'object_name': 'Offer'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'connector.skill': {
            'Meta': {'object_name': 'Skill'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['connector.Member']"})
        }
    }

    complete_apps = ['connector']