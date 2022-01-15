from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Investor, Project


@receiver(post_save, sender=Investor)
def investor_created(sender, instance: Investor, created, *args, **kwargs):
    if created:
        instance.remaining_amount = instance.total_amount
        instance.save()
