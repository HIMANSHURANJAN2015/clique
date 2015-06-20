"""
Definition of models.
"""

from django.db import models
from time import time
from datetime import datetime
from azurepython3.djangostorage import AzureStorage
from azurepython3.blobservice import BlobService

def get_upload_file_name(instance, filename):
    #return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)
    #assets/uploaded_files/%s_%s               
    return "assets/uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)


class Account(models.Model):
    email =models.EmailField(max_length=254,primary_key= True)
    password =models.CharField(max_length=20)
    name =models.CharField(max_length=50)
    dob_d=models.IntegerField(max_length=2)
    dob_m=models.IntegerField(max_length=2)
    dob_y=models.IntegerField(max_length=4)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.email

#####dekh posting azurepython ye sab hum daale hain
class Posting(models.Model):
    title = models.CharField(max_length=254)
    image = models.ImageField(max_length=255, storage=AzureStorage(account_name="******",account_key="******",container="new-public-container"),upload_to="images/postings") #container public rakho to help mile !!
    def get_thumbnail(self):
        thumb=str(self.pic)

class Accountinfo(models.Model):
    email = models.ForeignKey(Account,primary_key=True)
    #pic=models.FileField(upload_to=get_upload_file_name)
    pic=models.FileField(max_length=255, storage=AzureStorage(account_name="*****",account_key="******",container="new-public-container"),upload_to=get_upload_file_name) 
    #pic=models.ImageField(max_length=255, storage=AzureStorage(account_name="*****",account_key="*****",container="new-public-container"),upload_to="assets/uploaded_files/") 

    about=models.CharField(max_length=254)

    def get_thumbnail(self):
        thumb = str(self.pic)
        #if not settings.DEBUG:
        #    thumb = thumb.replace('assets/', '')
        return thumb
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.email
            
'''         
class Activity(models.Model):
    by =models.ForeignKey(Account)
    when =models.DateTimeField(default=datetime.now, blank=True)
    activity= models.CharField(max_length=254)      # uploade photot, shared photo ,thought
    data= models.CharField(max_length=254,null=True)
    photo=models.FileField(upload_to=get_upload_file_name,null=True)
    #like=models.IntegerField                        ab add nahi ho paega !! to add tis we are creating new model
    def get_thumbnail(self):
        thumb = str(self.photo)
        #if not settings.DEBUG:
        #    thumb = thumb.replace('assets/', '')
        return thumb 
'''

class Activity2(models.Model):
    by =models.ForeignKey(Account)
    when =models.DateTimeField(default=datetime.now, blank=True)
    activity= models.CharField(max_length=254)      # uploade photot, shared photo ,thought
    data= models.CharField(default="nothing",max_length=254,null=True)
    #photo=models.FileField(default="nothing",upload_to=get_upload_file_name,null=True)
    #photo=models.ImageField(default="nothing",max_length=255, storage=AzureStorage(account_name="*****",account_key="*****",container="new-public-container"),upload_to=get_upload_file_name) 
    photo=models.FileField(max_length=255, storage=AzureStorage(account_name="*****",account_key="******",container="new-public-container"),upload_to=get_upload_file_name) 
    like=models.IntegerField(default=0) 
    def get_thumbnail(self):
        thumb = str(self.photo)
        #if not settings.DEBUG:
        #    thumb = thumb.replace('assets/', '')
        return thumb 
    #def __str__(self):              # __unicode__ on Python 2
    #    return (self.by)
class FriendRequests(models.Model):
    #to_account= models.ForeignKey(Account,related_name='%(class)s_email')
    #from_account= models.ForeignKey(Account,related_name='%(class)s_email')
    from_account=models.ForeignKey(Account)
    to_account=models.CharField(max_length=254)
class Friends(models.Model):
    #this_account=models.ForeignKey(Account,related_name='%(class)s_email')
    #friend_account=models.ForeignKey(Account,related_name='%(class)s_email')
    this_account=models.ForeignKey(Account)
    friend_account=models.CharField(max_length=254)

class Ads(models.Model):
    name= models.CharField(max_length=30)
    about=models.CharField(max_length=254)
    link=models.CharField(max_length=50)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.name

class Channel(models.Model):
    name=models.CharField(max_length=30,primary_key=True)
    about=models.CharField(max_length=254)
    founder=models.ForeignKey(Account)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.name

class Subscriptions(models.Model):
    account_name=models.ForeignKey(Account)
    channel_name=models.ForeignKey(Channel)

class Channel_activity(models.Model):
    channel_name=models.ForeignKey(Channel)
    #pic=models.FileField(upload_to=get_upload_file_name,null=True)
    pic=models.ImageField(default="nothing",max_length=255, storage=AzureStorage(account_name="**",account_key="********",container="new-public-container"),upload_to=get_upload_file_name) 

    def get_thumbnail(self):
        thumb = str(self.pic)
        #if not settings.DEBUG:
        #    thumb = thumb.replace('assets/', '')
            
        return thumb 


     
