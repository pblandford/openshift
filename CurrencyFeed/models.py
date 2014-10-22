# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class CeleryTaskmeta(models.Model):
    id = models.IntegerField(primary_key=True)
    task_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True)
    hidden = models.BooleanField()
    meta = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'celery_taskmeta'

class CeleryTasksetmeta(models.Model):
    id = models.IntegerField(primary_key=True)
    taskset_id = models.CharField(max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'

class Currency(models.Model):
    name = models.CharField(max_length=3, blank=True)
    class Meta:
        managed = False
        db_table = 'currency'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class DjceleryCrontabschedule(models.Model):
    id = models.IntegerField(primary_key=True)
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)
    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'

class DjceleryIntervalschedule(models.Model):
    id = models.IntegerField(primary_key=True)
    every = models.IntegerField()
    period = models.CharField(max_length=24)
    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'

class DjceleryPeriodictask(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    interval = models.ForeignKey(DjceleryIntervalschedule, blank=True, null=True)
    crontab = models.ForeignKey(DjceleryCrontabschedule, blank=True, null=True)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True)
    exchange = models.CharField(max_length=200, blank=True)
    routing_key = models.CharField(max_length=200, blank=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'

class DjceleryPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'

class DjceleryTaskstate(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=64)
    task_id = models.CharField(max_length=36)
    name = models.CharField(max_length=200, blank=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True)
    kwargs = models.TextField(blank=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True)
    traceback = models.TextField(blank=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', blank=True, null=True)
    hidden = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'

class DjceleryWorkerstate(models.Model):
    id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'

class Pair(models.Model):
    base = models.CharField(max_length=3, blank=True)
    counter = models.CharField(max_length=3, blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'pair'

