from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms
from .models import Product, Review

class productForm(ModelForm):
    class Meta:
        model=Product
        #fields='__all__'
        fields= ['title','description','featured_image','tags']
        widgets={
            'tags': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(productForm,self).__init__(*args,**kwarg)

        #To add class attributes to each field individually
        #self.fields['title'].widget.attrs.update({'class' :'input','placeholder' :'Add Title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
class ReviewForm(ModelForm):
    class Meta:
        model=Review            
        fields=['value','body']
 

 
    def __init__(self, *args, **kwarg): # __init is constructor for class. invokes when class instance is created.
        super(ReviewForm,self).__init__(*args,**kwarg)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})        