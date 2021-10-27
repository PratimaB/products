from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from django.contrib import messages

from product.models import Product
from .models import Profile, Skill ,Message
from .utils import searchProfile,paginateProfile
from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm
# Create your views here.

def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method =='POST':
        username=request.POST['username']
        password =request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user does not exists")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user) # set user session to browser cookiee
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request,"username or password is incorrect")

        print(request.POST)
    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User logged out!')
    return redirect('login')
    
def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    
    if request.method == 'POST':

        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False) # holding data before save. just example below to show how it works
            user.username= user.username.lower()
            form.save()

            messages.success(request,'User account created!')
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,'Error is registration!')    

    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    search_query=''
    profiles,search_query= searchProfile(request)
    profiles,custom_range=paginateProfile(request,profiles,6)
    context= {'profiles':profiles,'search_query':search_query,
            'custom_range':custom_range}

    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    #get skills with desciptions and other without descriptions
    topskills=profile.skill_set.exclude(description="")
    otherskills=profile.skill_set.filter(description="")
    context ={'profile':profile ,'topskills' :topskills ,'otherskills' :otherskills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills=profile.skill_set.all()
    products= profile.product_set.all()
    context={'profile':profile,'skills':skills,'products':products}
    return render(request,'users/account.html',context)    

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    if request.method=="POST":
        form= ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context={'form':form}
    return render (request,'users/profile_form.html',context)

@login_required(login_url="login")
def createSkill(request):
        profile= request.user.profile
        form=SkillForm()

        if request.method =="POST":
            form=SkillForm(request.POST)

            if form.is_valid():
                skill= form.save(commit=False)
                skill.owner=profile
                form.save()
                messages.success(request,'Skill added.')
                return redirect('account')

        context={'form':form}
        return render(request,"users/skill_form.html",context)     

@login_required(login_url='login')
def editSkill(request,pk):
    profile= request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)
    if request.method=="POST":
        form= SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill updated')
            return redirect('account')

    context={'form':form}
    return render (request,'users/skill_form.html',context)  

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile=request.user.profile
    skill= profile.skill_set.get(id=pk)
    if request.method=="POST":
        skill.delete()
        messages.success(request,"Skill deleted.")
        return redirect('account')
    context={'object':skill}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request): 
    profile= request.user.profile
    messageRequests= profile.messages.all() # used related_name to ref recipient and avoid confusion with sender as both rewf to same field
    unreadCount= messageRequests.filter(is_read=False).count()
    
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def ViewMessage(request,pk): 
    profile= request.user.profile
    message= profile.messages.get(id=pk)    # used related_name to ref recipient and avoid confusion with sender as both rewf to same field
    if message.is_read == False:
        message.is_read=True
        message.save()

    context={'message':message}
    return render(request,'users/message.html',context)

def createMessage(request,pk,id):
    recipient = Profile.objects.get(id=pk)
    product=Product.objects.get(id=id)

    form= MessageForm()
    try:
        sender=request.user.profile
    except:
        sender=None

    if request.method=='POST':
        form= MessageForm(request.POST)
        if form.is_valid():
            message= form.save(commit=False)
            message.sender=sender
            message.recipient=recipient
            if sender: # if sender has valid email then pick up details from profile
                message.name= sender.name
                message.email= sender.email

            message.product_title=str(product)
            message.save()    
            messages.success(request,'Message sent')
            return redirect('products')
    context={'recipient':recipient,'product' :product ,'form':form}
    return render(request,'users/message_form.html',context)    
