from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def register(self, name, username, dob, email, password, confirm):
        errors = []
        if len(name) < 3:
            errors.append("Name must be 3 characters or more")
        
        if len(username) < 3:
            errors.append("Username must be 3 characters or more")
        
        if len(dob) < 1:
            errors.append("Date of Birth is required")
        else:
            day = datetime.strptime(dob, "%Y-%m-%d")
            if day > datetime.now():
                errors.append("Date of Birth must be in the past")

        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) > 0:
                errors.append("Email already in use")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                name=name,
                username=username,
                dob=dob,
                email=email.lower(),
                password=password
            )
        return response
        
    def login(self, username, password):
        errors = []

        if len(username) < 1:
            errors.append("username is required")
        elif not (username):
            errors.append("Invalid username")
        else:
            usersMatchingUsername = User.objects.filter(username=username)
            if len(usersMatchingUsername) == 0:
                errors.append("Unknown username")


        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "username": None 
        }

        if len(errors) == 0:
            if password == usersMatchingUsername[0].password:
                response["username"] = usersMatchingUsername[0]
            else:
                errors.append("Incorrect password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response

class User (models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    dob = models.DateTimeField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friend = models.ManyToManyField("self", related_name="friends", symmetrical=False)
    
    objects = UserManager()

    def __repr__(self):
        return "<User object:({}) {} {} {} {} {} >".format(self.id,self.name, self.username,self.dob,self.email, self.password)

# class QuoteManager(models.Manager):
# 	def validateQuote(self, post_data):

# 		is_valid = True
# 		errors = []

# 		if len(post_data.get('content')) < 12:
# 			is_valid = False
# 			errors.append('Message must be more than 10 characters')
# 		return (is_valid, errors)

# class Quote(models.Model):
# 	content = models.CharField(max_length = 255)
# 	author = models.CharField(max_length = 255)
# 	poster = models.ForeignKey(User, related_name = 'authored_quotes')
# 	created_at = models.DateTimeField(auto_now_add = True)
# 	updated_at = models.DateTimeField(auto_now = True)
# 	objects = QuoteManager()

# 	def __str__(self):
# 		return 'content:{}, author:{}'.format(self.content, self.user)