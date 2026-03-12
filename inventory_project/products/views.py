from django.db.models import ExpressionWrapper, F, FloatField, Max, Sum
from django.shortcuts import get_object_or_404, redirect, render

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

	search_query = request.GET.get('q', '').strip()
	filter_category = request.GET.get('category', '').strip()

	categories = Category.objects.order_by('name')
	products = Product.objects.select_related('category').order_by('-created_at')

	if search_query:
		products = products.filter(name__icontains=search_query)
	if filter_category:
		products = products.filter(category_id=filter_category)

	LOW_STOCK_THRESHOLD = 5

	stock_value_expr = ExpressionWrapper(
		F('price') * F('quantity'), output_field=FloatField()
	)
	agg = Product.objects.aggregate(
		total_qty=Sum('quantity'),
		total_value=Sum(stock_value_expr),
		max_price=Max('price'),
	)
	total_quantity  = agg['total_qty']   or 0
	total_value     = agg['total_value'] or 0
	max_price       = agg['max_price']   or 0

	out_of_stock_count = Product.objects.filter(quantity=0).count()
	low_stock_count    = Product.objects.filter(quantity__gt=0, quantity__lte=LOW_STOCK_THRESHOLD).count()

	# annotate filtered queryset with per-row stock value
	products = products.annotate(
		stock_value=ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField())
	)

	context = {
		'category_form': category_form,
		'product_form': product_form,
		'categories': categories,
		'products': products,
		'category_count': categories.count(),
		'product_count': Product.objects.count(),
		'total_quantity': total_quantity,
		'total_value': total_value,
		'max_price': max_price,
		'out_of_stock_count': out_of_stock_count,
		'low_stock_count': low_stock_count,
		'low_stock_threshold': LOW_STOCK_THRESHOLD,
		'search_query': search_query,
		'filter_category': filter_category,
	}
	return render(request, 'products/home.html', context)


def delete_category(request, pk):
	if request.method == 'POST':
		get_object_or_404(Category, pk=pk).delete()
	return redirect('home')


def edit_category(request, pk):
	category = get_object_or_404(Category, pk=pk)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = CategoryForm(instance=category)
	return render(request, 'products/edit_category.html', {'form': form, 'category': category})


def delete_product(request, pk):
	if request.method == 'POST':
		get_object_or_404(Product, pk=pk).delete()
	return redirect('home')


def edit_product(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = ProductForm(instance=product)
	return render(request, 'products/edit_product.html', {'form': form, 'product': product})
