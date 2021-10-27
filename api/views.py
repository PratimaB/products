from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from users.models import Profile
from .serializes import ProductSerializer
from product.models import Product,Review
  
@api_view(['GET'])
def getRoutes(request):

    routes=[
        {'GET':'/api/products'},
        {'GET':'/api/products/id'},
        {'POST':'/api/products/id/vote'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},

    ]
    # by default json returns dictionary , for json response safe =false makes json return more than dictionary
    # now Response is HTTP
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getProducts(request):
    print("User Is" , request.user)
    products= Product.objects.all()
    # we need to pass json (serialized data) ,   return Response(projects) will not work in 
    serializer=ProductSerializer(products,many=True) # single object or all
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    product= Product.objects.get(id=pk)
    # we need to pass json (serialized data) ,   return Response(projects) will not work in 
    serializer=ProductSerializer(product,many=False) # single object or all
    return Response(serializer.data)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def productVote(request,pk):
    product=Product.objects.get(id=pk)
    user= request.user.profile
    data= request.data
    print("data : ",data)
    review,created =Review.objects.get_or_create(
        owner=user,
        product=product,
    )
    review.value= data['value']
    review.save()
    product.getVoteCount
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)