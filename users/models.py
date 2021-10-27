from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.validators import RegexValidator

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE , null=True,blank=True)
    name= models.CharField(max_length=200, null=True,blank=True)
    username= models.CharField(max_length=200, null=True,blank=True)
    location= models.CharField(max_length=200, null=True,blank=True)
    email=models.EmailField(max_length=500, null= True,blank=True)
    short_intro=models.CharField(max_length=200,null=True,blank=True)
    bio= models.TextField(null=True,blank=True)
    profile_image= models.ImageField(null=True,blank = True,
                    upload_to='profiles/',default='profiles/user-default.png')
    social_linkedin= models.CharField(max_length=200, null=True,blank=True)
    social_youtube= models.CharField(max_length=200, null=True,blank=True)
    social_website= models.CharField(max_length=200, null=True,blank=True)  
    social_twitter= models.CharField(max_length=200, null=True,blank=True)               
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

    class Meta:
        ordering=['-created']                     

#def str(self): is a python method which is called when we use print/str to convert object into a string
    def __str__(self) :
        return str(self.username)            

    @property
    def imageProfile(self):
        try:
            url=self.profile_image.url
        except:
            url=""
        return url        

class Skill(models.Model):
    owner= models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200, null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)
    
    def __str__(self) :
        return str(self.name)                    
        
#related_name = need to specify else 2 times foreighkey to same model 'profile' will not be allowed
# pls read documentation for more uses and risk
class Message(models.Model):
    sender=models.ForeignKey(Profile,null=True,blank=True, on_delete= models.SET_NULL)
    recipient=models.ForeignKey(Profile,null=True,blank=True,
                    on_delete = SET_NULL,related_name="messages")
    name=models.CharField(max_length=200,null=True,blank=True) 
    contact = models.CharField(max_length=30,  null=True,blank=True) # validators should be a list
    email=models.EmailField(max_length=200,null=True,blank=True)                    
    subject=models.CharField(max_length=200,null=True,blank=True) 
    product_title=models.CharField(max_length=200,null=True,blank=True) 
    body=models.TextField()
    is_read= models.BooleanField(default=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

#   
    def __str__(self) :
        return self.subject                        

    class Meta:
        ordering=['is_read','-created'] # [-sigh before fieldname will do descending order]