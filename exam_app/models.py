from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        # check username in db
        email_list = User.objects.filter(email=post_data['email'])
        if len(email_list) == 0:
            # errors['username'] = 'Username not found'
            errors['email'] = 'There was a problem'

        # check password

        elif not bcrypt.checkpw(
            post_data['password'].encode(),  # from the form
            email_list[0].password.encode()  # from the db
        ):
            # errors['password'] = 'Password did not match'
            errors['password'] = 'There was a problem'
        return errors

    def register_validator(self, post_data):
        errors = {}
        # check username
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'first name must be longer than 2 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'last name must be longer than 2 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):           
            errors['email'] = "Invalid email address!"
        # check password
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'

        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = 'Password does not match'

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'email taken'
        return errors

class WishManager(models.Manager):
    def wish_validator(self, post_data):
        errors = {}
        if post_data['wish_item'] == '':
            errors['wish_item1'] = 'A wish must be provided'
        elif len(post_data['wish_item']) < 3:
            errors['wish_item'] = 'wish must be longer than 3 characters'
        if post_data['description'] =='':
            errors['description1'] = 'A description must be provided'
        elif len(post_data['description']) < 3:
            errors['description'] = 'description must be longer than 3 characters'
        return errors

class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    objects=UserManager()

class Wish(models.Model):
    wish_item= models.CharField(max_length=255)
    description= models.TextField()
    wished_by= models.ForeignKey(
        User, related_name='wishes', on_delete=models.CASCADE)
    liked_by= models.ManyToManyField(User, related_name='likes')
    granted= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add = True)
    updated_at= models.DateTimeField(auto_now= True)
    objects=WishManager()