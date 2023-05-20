# Generated by Django 3.2.19 on 2023-05-16 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_auto_20230511_0909'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredientinrecipe',
            name='unique ingredient',
        ),
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='unique_following',
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_subscribing'),
        ),
    ]
