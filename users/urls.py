from django.contrib import messages
from django.urls import path
from .import views

urlpatterns = [

    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
    

    path('user-profile/',views.userProfile,name='user-profile'),
    path('account/',views.userAccount,name='account'),
    path('edit-account/',views.editAccount,name='edit-account'),

    # path('create-skill/',views.createSkill,name='create-skill'),
    # path('edit-skill/<str:pk>',views.editSkill,name='edit-skill'),
    # path('delete-skill/<str:pk>',views.deleteSkill,name='delete-skill'),

    path('inbox/',views.inbox,name='inbox'),
    path('message/<str:pk>',views.ViewMessage ,name='message'),
    path('create-message/<str:pk>/<str:id>/',views.createMessage ,name='create-message'),
]
