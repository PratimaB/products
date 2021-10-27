from rest_framework import fields, serializers
from product.models import Product ,Tag ,Review
from users.models import Profile

# here we are serializing model , we can serialize dictionary etc..

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields='__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    # previously we were getting profile and tag objects. we need actual values
    #reassign values of owner and tag
    owner = ProfileSerializer(many=False) # we have only 1 profile for project
    tags=TagSerializer(many=True) # we have many tags for 1 project
    reviews = serializers.SerializerMethodField() # attach get_'nameof field' to write get method for the same 
    class Meta:
        model= Product
        fields='__all__'

    def get_reviews(self,obj):
        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return serializer.data

        