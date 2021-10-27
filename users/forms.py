from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Skill,Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields=['first_name','email','username',
                'password1','password2']
        labels= {'first_name':'Name',
                  'email':'Email','username':'User Name',
                  'password1':'Password','password2':'Confirm password'
                }

    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(CustomUserCreationForm,self).__init__(*args,**kwarg)

        #To add class attributes to each field individually
        #self.fields['title'].widget.attrs.update({'class' :'input','placeholder' :'Add Title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
                
        
class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields=['name','email','username','location','short_intro',
                'bio','profile_image','social_linkedin',
                'social_youtube','social_website','social_twitter']

    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(ProfileForm,self).__init__(*args,**kwarg)

        #To add class attributes to each field individually
        #self.fields['title'].widget.attrs.update({'class' :'input','placeholder' :'Add Title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class SkillForm(ModelForm):
    class Meta:
        model=Skill
        fields="__all__"
        exclude=['owner']

    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(SkillForm,self).__init__(*args,**kwarg)

    #To add class attributes to each field individually
    #self.fields['title'].widget.attrs.update({'class' :'input','placeholder' :'Add Title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model=Message
        fields=['name','email','contact','subject','body']

    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(MessageForm,self).__init__(*args,**kwarg)

        #To add class attributes to each field individually
        self.fields['name'].widget.attrs.update({'class' :'input','placeholder' :'Enter Name','required':True})
        self.fields['email'].widget.attrs.update({'class' :'input','placeholder' :'Enter Email','required':False})
        self.fields['contact'].widget.attrs.update({'class' :'input','placeholder' :'Enter Contact No.','required':True})
        self.fields['subject'].widget.attrs.update({'class' :'input','placeholder' :'Enter Subject','required':True})
        self.fields['body'].widget.attrs.update({'class' :'input','placeholder' :'Enter Enquiry','required':True})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
