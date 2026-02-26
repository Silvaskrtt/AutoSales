from django.conf import settings
from django.db import models
from django.urls import reverse


class Relatorio(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	file = models.FileField(upload_to='relatorios/', null=True, blank=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "Relatório"
		verbose_name_plural = "Relatórios"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('relatorios:detail', args=[self.slug])
