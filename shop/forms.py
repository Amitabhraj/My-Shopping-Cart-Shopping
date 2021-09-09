from django import forms
from . models import *  

class MyfileUploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file_subcategory = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file_price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))



class products(forms.ModelForm):  
    class Meta:  
        model = Product
        fields = "__all__"  
