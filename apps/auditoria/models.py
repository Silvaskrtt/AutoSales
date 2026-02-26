from django.db import models

from accounts.models import User

class LogAcesso(models.Model):
    id_log = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_log} - {self.data_hora} - {self.acao} - {self.user.username}"

class LogSistema(models.Model):
    id_log = models.AutoField(primary_key=True)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50)
    data_hora = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Only save LogSistema when a user is available.

        If `self.user` is not set, try to get the current request user from
        thread-local storage (`auditoria.threadlocals.get_current_user`). If
        still not available, do not create the log (no-op).
        """
        if not self.user:
            try:
                from .threadlocals import get_current_user
                current = get_current_user()
            except Exception:
                current = None
            if current:
                self.user = current
            else:
                # sem usuário, não insere o LogSistema
                return
        super().save(*args, **kwargs)

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    )

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    object_repr = models.TextField(blank=True)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.CharField(max_length=45, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.get_action_display()} - {self.content_type.app_label}.{self.content_type.model} ({self.object_id})"