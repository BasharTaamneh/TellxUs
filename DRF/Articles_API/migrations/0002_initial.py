# Generated by Django 4.0 on 2022-03-14 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Articles_API', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to='accounts.usermodel'),
        ),
        migrations.AddField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to='accounts.usermodel'),
        ),
        migrations.AddField(
            model_name='articlefiles',
            name='article_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Articles_API.article'),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='article_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Articles_API.article'),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.usermodel'),
        ),
        migrations.AddField(
            model_name='articlecomments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='Articles_API.articlecomments'),
        ),
        migrations.AddField(
            model_name='article',
            name='anger_me',
            field=models.ManyToManyField(blank=True, related_name='anger_me', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='love_it',
            field=models.ManyToManyField(blank=True, related_name='love_it', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.usermodel'),
        ),
    ]
