from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category name'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'placeholder': '0', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        session_key = kwargs.pop('session_key', None)
        super().__init__(*args, **kwargs)

        if session_key:
            self.fields['category'].queryset = Category.objects.filter(session_key=session_key).order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.none()
