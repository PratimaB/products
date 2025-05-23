from django.db import models
import uuid
from users.models import Profile
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models import Q

# Create your models here.
class Product(models.Model):
    owner= models.ForeignKey(Profile, blank = True, null= True,on_delete=SET_NULL)
    title = models.CharField(max_length= 200)
    description = models.TextField(null = True,blank = True)
    featured_image=models.ImageField(null=True,blank=True,default='default.jpg')

    tags = models.ManyToManyField('Tag',blank=True) # from Tag model relationship
    total_vote = models.IntegerField(default=0,null=True)
    vote_ratio = models.IntegerField(default=0,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4,unique=True,
                        primary_key=True,editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-vote_ratio','-total_vote','title']

    # Flat=True will return and not object
    @property
    def imageURL(self):
        try:
            url=self.featured_image.url
        except:
            url=""    
        return url

    @property 
    def reviewers(self):
        queryset=self.review_set.all().values_list('owner__id',flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews=self.review_set.all()
        upVotes=reviews.filter(value='up').count()
        totalVotes=reviews.count()
        ratio= (upVotes/totalVotes)*100
        self.total_vote=totalVotes
        self.vote_ratio=ratio
        self.save()

class Review(models.Model):
    VOTE_TYPE=(
        ('up','up vote'),
        ('down','down vote'),
    )
    # delete reviews on deletetion of user from profile
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE , null=True)
    product= models.ForeignKey(Product, on_delete = models.CASCADE)        
    body=models.TextField(blank=True,null=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default =uuid.uuid4, unique=True,
                        editable=False,primary_key=True)

    class Meta:
        unique_together=[['owner','product']] # no user can review multiple times for one product

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default =uuid.uuid4, unique=True,
                        editable=False,primary_key=True)

    def __str__(self) :
        return self.name                    



