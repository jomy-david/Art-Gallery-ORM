from django.db import models

# Create your models here.

class artist_list(models.Model):
    name = models.CharField(max_length=30)
    artist_id = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    contact = models.BigIntegerField()
    profile_pic = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    display_name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    status = models.IntegerField()
    posts = models.BigIntegerField()

class category_list(models.Model):
    cat_id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=20)
    posts = models.BigIntegerField()

class comments(models.Model):
    post_id = models.IntegerField()
    user_id = models.CharField(max_length=20)
    comment = models.CharField(max_length=60)
    spam = models.IntegerField()

class commentspam(models.Model):
    comment_id = models.IntegerField()
    user_id = models.CharField(max_length=30)

class like_list(models.Model):
    user_id = models.CharField(max_length=30)
    post_id = models.IntegerField()

class logintb(models.Model):
    user_id = models.CharField(max_length=30)
    user_type = models.CharField(max_length=20)
    status = models.IntegerField()
    password = models.CharField(max_length=30)

class messages_table(models.Model):
    sender_id = models.CharField(max_length=30)
    reciever_id = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    status = models.IntegerField()

class post_list(models.Model):
    post_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=30)
    artist_id = models.CharField(max_length=30)
    category = models.CharField(max_length=20)
    cat_id  = models.IntegerField()
    status = models.IntegerField()
    title = models.CharField(max_length=30)
    likes = models.IntegerField()
    comments = models.IntegerField()

class user_list(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    contact = models.BigIntegerField()
    profile_pic = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    status = models.IntegerField()

class test(models.Model):
    new_id = models.IntegerField()

