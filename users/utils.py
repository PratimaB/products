from .models import Profile, Skill 
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProfile(request,profiles,results):
    #results- number of records per page
    page=request.GET.get('page')
    paginator=Paginator(profiles,results)

    # reassign projects to first page data
    try:
        profiles=paginator.page(page)
    except PageNotAnInteger:
            page=1
            profiles=paginator.page(page)
    except EmptyPage:
            page = paginator.num_pages
            profiles=paginator.page(page)

    leftIndex= (int(page)-1)
    if leftIndex <1:
        leftIndex=1

    rightIndex=(int(page)+4)    
    if rightIndex>=paginator.num_pages:
        rightIndex=paginator.num_pages +1
    custom_range= range(leftIndex,rightIndex)
    return profiles,custom_range

def searchProfile(request):

    search_query=''
    if request.GET.get('search_query'):
        search_query= request.GET.get('search_query')

    skills= Skill.objects.filter(name__icontains=search_query)

    #profiles= Profile.objects.all()
    #search filter modification else to show all above statement
    # use '|' for 'OR' & for 'AND' filter
    #seach for skill too
    profiles= Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
 
    return profiles,search_query
