from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer, Version

@receiver(post_save, sender=Customer)
@receiver(post_delete, sender=Customer)
def version_update(sender, instance, **kwargs):
    version, created = Version.objects.get_or_create(id=1)
    version.update_version()
    print('Version Created')