from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product,Tag
from .forms import productForm,ReviewForm
from .utils import searchProduct,paginateProduct
from django.contrib import messages
# Create your views here.

def products(request):
    products,search_query=searchProduct(request)

    products,custom_range =paginateProduct(request,products,6)
    context ={'products' :products,'search_query':search_query,'custom_range':custom_range}
    return render(request,'product/products.html',context)

def product(request,pk):
    productObj= Product.objects.get(id=pk)
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.product=productObj
            review.owner= request.user.profile
            review.save()
            # update product vote count 
            productObj.getVoteCount
            
            messages.success(request,"Your review submitted successfully.")
            return redirect('product',pk=productObj.id)


    return render(request,'product/single-product.html',{'product': productObj ,'form':form})

@login_required(login_url='login')
def createProduct(request):
    profile= request.user.profile
    form = productForm()
    if request.method =='POST':
        form= productForm(request.POST,request.FILES)
        if form.is_valid():
            # when user added new project it should refect to main account page hence 
            # assign new project 
            product=form.save(commit=False)
            product.owner=profile
            product.save()
            return redirect('account')

    context={'form':form}
    return render(request,'product/product_form.html',context)    

login_required(login_url='login')
def updateProduct(request,pk):
    profile=request.user.profile
    product=profile.product_set.get(id=pk)
    form = productForm(instance = product)


    if request.method =='POST':
        form= productForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request,'product/product_form.html',context)     

login_required(login_url='login')
def deleteProduct(request,pk):
    profile=request.user.profile
    product=profile.product_set.get(id=pk)
    if request.method =='POST':
        product.delete()
        return redirect('products')

    context={'object':product}
    return render(request,'delete_template.html',context)     