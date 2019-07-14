# Generated by Django 3.0 on 2019-07-14 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0003_postagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curtida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curti', to='perfis.Perfil')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curtidas', to='perfis.Postagem')),
            ],
        ),
    ]
