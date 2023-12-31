# Generated by Django 4.2.5 on 2023-10-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='artist_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('artist_id', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('contact', models.IntegerField(max_length=10)),
                ('profile_pic', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('display_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=60)),
                ('status', models.IntegerField(max_length=1)),
                ('posts', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='category_list',
            fields=[
                ('cat_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('posts', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('user_id', models.CharField(max_length=20)),
                ('comment', models.CharField(max_length=60)),
                ('spam', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='commentspam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.IntegerField()),
                ('user_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='like_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30)),
                ('post_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='logintb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30)),
                ('user_type', models.CharField(max_length=20)),
                ('status', models.IntegerField()),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='messages_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.CharField(max_length=30)),
                ('reciever_id', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=100)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='post_list',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=100)),
                ('artist_name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=20)),
                ('cat_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('title', models.CharField(max_length=30)),
                ('likes', models.IntegerField()),
                ('comments', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('contact', models.IntegerField(max_length=10)),
                ('profile_pic', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('status', models.IntegerField()),
            ],
        ),
    ]
