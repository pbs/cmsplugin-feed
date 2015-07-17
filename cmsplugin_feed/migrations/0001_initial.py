# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='name', blank=True)),
                ('feed_url', models.URLField(verbose_name='feed URL')),
                ('paginate_by', models.IntegerField(default=5, null=True, verbose_name=b'paginate by', blank=True)),
            ],
            options={
                'db_table': 'cmsplugin_feed',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
