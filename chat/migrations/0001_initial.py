# Generated by Django 3.1.1 on 2020-10-09 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.dialog')),
            ],
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('abstractfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='file.abstractfile')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='chat.message')),
            ],
            bases=('file.abstractfile', models.Model),
        ),
        migrations.CreateModel(
            name='DialogMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.dialog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
