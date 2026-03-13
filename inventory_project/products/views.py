from django.db.models import ExpressionWrapper, F, FloatField, Max, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ProductForm
from .models import Category, Product


def _get_session_key(request):
	if not request.session.session_key:
		request.session.create()
	return request.session.session_key


def home(request):
	session_key = _get_session_key(request)
	category_form = CategoryForm()
	product_form = ProductForm(session_key=session_key)

	if request.method == 'POST':
		form_type = request.POST.get('form_type')

		if form_type == 'category':
			category_form = CategoryForm(request.POST)
			if category_form.is_valid():
				category = category_form.save(commit=False)
				category.session_key = session_key
				category.save()
				return redirect('home')
		elif form_type == 'product':
			product_form = ProductForm(request.POST, session_key=session_key)
			if product_form.is_valid():
				product = product_form.save(commit=False)
				product.session_key = session_key
				product.save()
				return redirect('home')

	search_query = request.GET.get('q', '').strip()
	filter_category = request.GET.get('category', '').strip()

	categories = Category.objects.filter(session_key=session_key).order_by('name')
	products = Product.objects.filter(session_key=session_key).select_related('category').order_by('-created_at')

	if search_query:
		products = products.filter(name__icontains=search_query)
	if filter_category:
		products = products.filter(category_id=filter_category)

	LOW_STOCK_THRESHOLD = 5

	stock_value_expr = ExpressionWrapper(
		F('price') * F('quantity'), output_field=FloatField()
	)
	agg = Product.objects.filter(session_key=session_key).aggregate(
		total_qty=Sum('quantity'),
		total_value=Sum(stock_value_expr),
		max_price=Max('price'),
	)
	total_quantity  = agg['total_qty']   or 0
	total_value     = agg['total_value'] or 0
	max_price       = agg['max_price']   or 0

	out_of_stock_count = Product.objects.filter(session_key=session_key, quantity=0).count()
	low_stock_count    = Product.objects.filter(session_key=session_key, quantity__gt=0, quantity__lte=LOW_STOCK_THRESHOLD).count()

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
		'product_count': Product.objects.filter(session_key=session_key).count(),
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
	session_key = _get_session_key(request)
	if request.method == 'POST':
		get_object_or_404(Category, pk=pk, session_key=session_key).delete()
	return redirect('home')


def edit_category(request, pk):
	session_key = _get_session_key(request)
	category = get_object_or_404(Category, pk=pk, session_key=session_key)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			updated_category = form.save(commit=False)
			updated_category.session_key = session_key
			updated_category.save()
			return redirect('home')
	else:
		form = CategoryForm(instance=category)
	return render(request, 'products/edit_category.html', {'form': form, 'category': category})


def delete_product(request, pk):
	session_key = _get_session_key(request)
	if request.method == 'POST':
		get_object_or_404(Product, pk=pk, session_key=session_key).delete()
	return redirect('home')


def edit_product(request, pk):
	session_key = _get_session_key(request)
	product = get_object_or_404(Product, pk=pk, session_key=session_key)
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product, session_key=session_key)
		if form.is_valid():
			updated_product = form.save(commit=False)
			updated_product.session_key = session_key
			updated_product.save()
			return redirect('home')
	else:
		form = ProductForm(instance=product, session_key=session_key)
	return render(request, 'products/edit_product.html', {'form': form, 'product': product})
