# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Domain'
        db.create_table('connector_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('connector', ['Domain'])

        # Adding model 'Member'
        db.create_table('connector_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['connector.Domain'])),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['auth.User'])),
            ('is_setup', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('connector', ['Member'])

        # Adding model 'Category'
        db.create_table('connector_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['connector.Category'])),
        ))
        db.send_create_signal('connector', ['Category'])

        # Adding model 'Skill'
        db.create_table('connector_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['connector.Member'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['connector.Category'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('connector', ['Skill'])

        # Adding unique constraint on 'Skill', fields ['member', 'category']
        db.create_unique('connector_skill', ['member_id', 'category_id'])

        # Adding model 'Offer'
        db.create_table('connector_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(max_length=50, populate_from='title', unique_with=())),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['connector.Category'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['connector.Member'])),
            ('state', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('bid_low', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5, default=0)),
            ('bid_high', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5, default=0)),
        ))
        db.send_create_signal('connector', ['Offer'])


    def backwards(self, orm):
        # Removing unique constraint on 'Skill', fields ['member', 'category']
        db.delete_unique('connector_skill', ['member_id', 'category_id'])

        # Deleting model 'Domain'
        db.delete_table('connector_domain')

        # Deleting model 'Member'
        db.delete_table('connector_member')

        # Deleting model 'Category'
        db.delete_table('connector_category')

        # Deleting model 'Skill'
        db.delete_table('connector_skill')

        # Deleting model 'Offer'
        db.delete_table('connector_offer')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'connector.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['connector.Category']"})
        },
        'connector.domain': {
            'Meta': {'object_name': 'Domain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'connector.member': {
            'Meta': {'object_name': 'Member'},
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['connector.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_setup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"})
        },
        'connector.offer': {
            'Meta': {'object_name': 'Offer'},
            'bid_high': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5', 'default': '0'}),
            'bid_low': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5', 'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['connector.Category']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['connector.Member']"}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'state': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'connector.skill': {
            'Meta': {'unique_together': "(('member', 'category'),)", 'object_name': 'Skill'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['connector.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['connector.Member']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['connector']