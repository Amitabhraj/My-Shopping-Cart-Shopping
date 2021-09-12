from django import forms
from . models import *  

class MyfileUploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Enter Product Name"}))
    file_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Enter Product category"}))
    file_subcategory = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Enter Product Subcategory"}))
    file_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Don't write '$' before price, Enter Just Price in Number"}))
    file_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))



class products(forms.ModelForm):  
    class Meta:  
        model = Product
        fields = "__all__"  
