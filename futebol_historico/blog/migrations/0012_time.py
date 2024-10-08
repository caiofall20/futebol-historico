# Generated by Django 5.0.6 on 2024-06-23 19:36

import ckeditor_uploader.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_selecao_regiao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='times/')),
                ('descricao', ckeditor_uploader.fields.RichTextUploadingField()),
                ('fundacao', models.DateField(default=django.utils.timezone.now)),
                ('titulos', models.IntegerField(default=0)),
                ('regiao', models.CharField(choices=[('América do Sul', 'América do Sul'), ('América Central', 'América Central'), ('Europa', 'Europa'), ('África', 'África'), ('Ásia', 'Ásia')], default='Europa', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
