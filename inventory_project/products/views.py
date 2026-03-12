from django.shortcuts import render

from .forms import CategoryForm, ProductForm


def home(request):
	context = {
		'category_form': CategoryForm(),
		'product_form': ProductForm(),
	}
	return render(request, 'products/home.html', context)
