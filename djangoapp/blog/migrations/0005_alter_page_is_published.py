# Generated by Django 4.2.1 on 2023-05-23 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_page_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Deixe Marcado Para Exibir Essa Página !'),
        ),
    ]
