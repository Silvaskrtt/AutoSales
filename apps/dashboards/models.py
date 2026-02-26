from django.conf import settings
from django.db import models
from django.urls import reverse


class Dashboard(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
	)
	is_public = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at", "-created_at"]
		verbose_name = "Dashboard"
		verbose_name_plural = "Dashboards"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("dashboards:detail", args=[self.slug])
