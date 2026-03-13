from django.conf import settings
from django.db import models


class Category(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='categories',
		null=True,
		blank=True,
	)
	session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Product(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='products',
		null=True,
		blank=True,
	)
	session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
	name = models.CharField(max_length=150)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
