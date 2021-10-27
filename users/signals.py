
# Signal is called any time when save method of Profile is fired.
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings
# receiver signal
#@receiver(post_save,sender=User)
def CreateProfile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        # send email when user created 1st time
        subject='Welcome new user'
        message ='Thank for registering with us.'
        send_mail(
            subject,
            message ,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )    


#when user edits profile , need to update user too
def updateUser(sender,instance, created,**kwargs):
    profile=instance
    user=profile.user
    # created=false is required ,else createprofile will call updateuser and vice versa creating infinite loop
    if created==False: 
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()
# when profile is deleted delete user too
def deleteUser(sender,instance, **kwargs):
    user= instance.user
    user.delete()


# any time user is created default profile with some values is created.
# no nned to write deleteProfile as CASCADE in Profile model will take care.
#  When user is deleted profile will get deleted.

post_save.connect(CreateProfile,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)
# above and @receiver(post_save,Profile) are the same ways to trigger signal