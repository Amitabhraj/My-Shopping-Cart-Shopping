from django import forms
from . models import *  

class MyfileUploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Enter Product Name"}))
    file_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':"Enter the Price of the Product",'style': 'width: 450px !important;'}))
    file_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))



class products(forms.ModelForm):  
    class Meta:  
        model = Product
        fields = "__all__"  
