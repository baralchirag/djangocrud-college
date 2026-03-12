from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import CategoryForm, ProductForm
from .models import Category, Product


def home(request):
	category_form = CategoryForm()
	product_form = ProductForm()

	if request.method == 'POST':
		form_type = request.POST.get('form_type')

		if form_type == 'category':
			category_form = CategoryForm(request.POST)
			if category_form.is_valid():
				category_form.save()
				return redirect('home')
		elif form_type == 'product':
			product_form = ProductForm(request.POST)
			if product_form.is_valid():
				product_form.save()
				return redirect('home')

	categories = Category.objects.order_by('name')
	products = Product.objects.select_related('category').order_by('-created_at')
	total_quantity = Product.objects.aggregate(t=Sum('quantity'))['t'] or 0

	context = {
		'category_form': category_form,
		'product_form': product_form,
		'categories': categories,
		'products': products,
		'category_count': categories.count(),
		'product_count': products.count(),
		'total_quantity': total_quantity,
	}
	return render(request, 'products/home.html', context)
