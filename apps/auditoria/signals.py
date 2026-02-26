from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from .models import AuditLog
from django.conf import settings
from .threadlocals import get_current_user, get_current_ip

# Cache previous state before save to compute changes
_PRE_SAVE_CACHE = {}


def _key_for_instance(instance):
    return (instance._meta.label_lower, getattr(instance, 'pk', None))


@receiver(pre_save)
def auditoria_pre_save(sender, instance, **kwargs):
    # only for concrete models in our project apps
    if sender._meta.abstract:
        return
    if getattr(sender._meta, 'app_label', None) not in getattr(settings, 'AUDIT_LOG_MODELS_APPS', []):
        return
    if getattr(instance, 'pk', None):
        try:
            old = sender.objects.filter(pk=instance.pk).first()
            if old:
                _PRE_SAVE_CACHE[_key_for_instance(instance)] = model_to_dict(old)
        except Exception:
            pass


@receiver(post_save)
def auditoria_post_save(sender, instance, created, **kwargs):
    if sender._meta.abstract:
        return
    if getattr(sender._meta, 'app_label', None) not in getattr(settings, 'AUDIT_LOG_MODELS_APPS', []):
        return

    ct = ContentType.objects.get_for_model(sender)
    user = None
    # try to get ._audit_user if view set it on instance (optional)
    if hasattr(instance, '_audit_user') and instance._audit_user is not None:
        user = instance._audit_user
    else:
        # fallback to thread-local current user set by middleware
        user = get_current_user()

    new = model_to_dict(instance)
    key = _key_for_instance(instance)
    old = _PRE_SAVE_CACHE.pop(key, None)

    changes = None
    action = 'create' if created else 'update'
    if old:
        diffs = {}
        for k, newv in new.items():
            oldv = old.get(k)
            if oldv != newv:
                diffs[k] = {'old': oldv, 'new': newv}
        changes = diffs or None

    AuditLog.objects.create(
        action=action,
        user=user,
        content_type=ct,
        object_id=str(getattr(instance, 'pk', '')),
        object_repr=str(instance),
        changes=changes,
        ip_address=get_current_ip(),
    )


@receiver(post_delete)
def auditoria_post_delete(sender, instance, **kwargs):
    if sender._meta.abstract:
        return
    if getattr(sender._meta, 'app_label', None) not in getattr(settings, 'AUDIT_LOG_MODELS_APPS', []):
        return

    ct = ContentType.objects.get_for_model(sender)
    AuditLog.objects.create(
        action='delete',
        user=get_current_user(),
        content_type=ct,
        object_id=str(getattr(instance, 'pk', '')),
        object_repr=str(instance),
        changes=model_to_dict(instance),
        ip_address=get_current_ip(),
    )
