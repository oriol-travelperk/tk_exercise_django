# Generated by Django 3.0 on 2019-12-13 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20191212_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipe.Recipe'),
        ),
    ]