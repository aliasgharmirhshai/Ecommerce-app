# forms.py
from django import forms
from .models import Category

class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    min_rating = forms.DecimalField(required=False, min_value=0, max_value=5)