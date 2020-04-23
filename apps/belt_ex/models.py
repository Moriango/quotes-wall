from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _

EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
NAME_REGEX =  re.compile('[0-9]')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # email validations
        if len(postData["email"]) < 5:
            errors["email"] = "Email cannot be less than 5 characters"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Email invalid"

        # first name validations
        if (len(postData["fname"]) < 2) or  NAME_REGEX.search(postData["fname"]):
            errors["fname"] = "First name should be more than 2 characters and must not contain any numbers"

        # last name validations
        if (len(postData["lname"]) < 2) or  NAME_REGEX.search(postData["lname"]):
            errors["lname"] = "Last name should be more than 2 characters and must not contain any numbers"

        # password validations
        if len(postData["password"]) < 6:
            errors["password"] = "Password needs to be at least 6 characters"
        if postData["password"] != postData["pswd_confirm"]:
            errors["pswd_confirm"] = "Passwords don't match"
        # email duplication validation
        if len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "Email already exist" 
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['login_email']) < 1:
            errors["login_email"] = "Email does not exist"
        # email validations for login
        if len(postData["login_email"]) < 5:
            errors["login_email"] = "Email cannot be less than 5 characters"
        if not EMAIL_REGEX.match(postData["login_email"]):
            errors["login_email"] = "Email invalid" 
        # password validations for login
        if len(postData["login_password"]) < 6:
            errors["password"] = "Password needs to be at least 6 characters"
        return errors
 
    def quotes_validator(self, postData):
        errors = {}
        if len(postData["author"]) < 1:
            errors["author"] = "Author Name cannot be blank"
        if len(postData["content"]) < 1:
            errors["content"] = "Quote cannot be left blank"
        return errors
    def edit_validator(self, postData):
        errors = {}
        # email validations
        if len(postData["email"]) < 5:
            errors["email"] = "Email cannot be less than 5 characters"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Email invalid"

        # first name validations
        if (len(postData["fname"]) < 2) or  NAME_REGEX.search(postData["fname"]):
            errors["fname"] = "First name should be more than 2 characters and must not contain any numbers"

        # last name validations
        if (len(postData["lname"]) < 2) or  NAME_REGEX.search(postData["lname"]):
            errors["lname"] = "Last name should be more than 2 characters and must not contain any numbers"

        return errors

class User(models.Model):
    # id
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField((), max_length=254)
    password = models.CharField(max_length=255)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    # connected to the User validator
    objects = UserManager()




class Quotes(models.Model):
    # id
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    # connected to User Model
    posted_by = models.ForeignKey(User, related_name="user_quote", on_delete=models.PROTECT)
    users_liked = models.ManyToManyField(User, related_name="quotes_liked")

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    objects = UserManager()


# Create your models here.
