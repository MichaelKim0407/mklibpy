from django.db import migrations

__author__ = 'Michael'


def forward_func(apps, schema_editor):
    App = apps.get_model('app_manager', 'App')
    db_alias = schema_editor.connection.alias
    App.objects.using(db_alias).bulk_create([
        App(order=0, name='admin', active=True),
    ])


def reverse_func(apps, schema_editor):
    App = apps.get_model('app_manager', 'App')
    db_alias = schema_editor.connection.alias
    App.objects.using(db_alias).filter(name='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func)
    ]
