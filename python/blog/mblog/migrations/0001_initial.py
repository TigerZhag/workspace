# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 17:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.CharField(max_length=500)),
                ('isDeleted', models.BooleanField()),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('isDeleted', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PostDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('content', models.TextField()),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mblog.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('createdDate', models.DateField()),
                ('active', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='topicId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mblog.Topic'),
        ),
        migrations.AddField(
            model_name='comment',
            name='ownerId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mblog.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='postID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mblog.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='replyId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mblog.Comment'),
        ),
    ]
