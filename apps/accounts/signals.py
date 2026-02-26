import logging
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Create default groups and assign sensible permissions.

    Groups created: 'Admin' (full perms for core apps) and 'Vendedor' (limited perms).
    This function is idempotent and can be run multiple times.
    """
    try:
        app_labels_admin = [
            'clientes', 'veiculos', 'vendas', 'pagamentos',
            'financiamentos', 'parcelas', 'relatorios', 'dashboards',
        ]

        # Create or get Admin group and assign all permissions for listed apps
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_perms = Permission.objects.filter(content_type__app_label__in=app_labels_admin)
        admin_group.permissions.set(admin_perms)

        # Create or get Vendedor group with limited permissions
        vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')

        vendedor_full_apps = ['vendas', 'clientes', 'veiculos']
        vendedor_view_only = ['pagamentos', 'parcelas', 'financiamentos', 'relatorios', 'dashboards']

        # Django ORM doesn't support startswith multiple values directly; build queryset manually
        from django.db.models import Q
        q_full = Q()
        for app in vendedor_full_apps:
            q_full |= Q(content_type__app_label=app)
        q_full &= (Q(codename__startswith='add_') | Q(codename__startswith='change_') | Q(codename__startswith='view_'))
        vendedor_perms = Permission.objects.filter(q_full)

        # view only for other apps
        q_view = Q()
        for app in vendedor_view_only:
            q_view |= Q(content_type__app_label=app)
        q_view &= Q(codename__startswith='view_')
        vendedor_perms = vendedor_perms | Permission.objects.filter(q_view)

        vendedor_group.permissions.set(vendedor_perms.distinct())

        logger.info('Default groups ensured: Admin and Vendedor')
    except Exception as exc:
        logger.exception('Error creating default groups: %s', exc)
