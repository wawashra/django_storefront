# Generated by Django 3.2.4 on 2023-02-19 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name', 'user__last_name'], 'permissions': [('view_history', 'Can view history')]},
        ),
    ]