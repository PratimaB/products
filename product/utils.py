from .models import Product,Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProduct(request,products,results):
    page=request.GET.get('page')
    paginator=Paginator(products,results)

    # reassign products to first page data
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
            page=1
            products=paginator.page(page)
    except EmptyPage:
            page = paginator.num_pages
            products=paginator.page(page)

    leftIndex= (int(page)-1)
    if leftIndex <1:
        leftIndex=1

    rightIndex=(int(page)+4)    
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages +1

    custom_range= range(leftIndex,rightIndex)
    return products,custom_range

def searchProduct(request):
        search_query=''
        if request.GET.get('search_query'):
            search_query= request.GET.get('search_query')

        #Tag search is many to many - 1st search tag 
        tagsearch= Tag.objects.filter(name__icontains=search_query)

        #owner__name__icontain will search for owner's name ..
        products = Product.objects.distinct().filter(
            Q(title__icontains=search_query)|
            Q(description__icontains=search_query)|
            Q(owner__name__icontains=search_query)|
            Q(tags__in=tagsearch)
        )
        return products,search_query