from django.utils.translation import gettext_lazy as _

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, Profile
from dashboard.models import Shop
from vendors.managers import StaffManager


class Staff(User):
    objects = StaffManager()
    JOB_CHOICES = [
        ('owner', _('Shop Manager')),
        ('operator', _('Supervisor')),
        ('manager', _('Product Manager'))
    ]
    type = models.CharField(max_length=100, choices=JOB_CHOICES, verbose_name=_("Job Type"))
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='staff_shop', verbose_name=_("Shop"))

    class Meta:
        verbose_name = _("Staff")
        verbose_name_plural = _("Staffs")
        permissions = [
            ("is_owner", "Is owner"),
            ("is_manager", "Is manager")
        ]

    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = False
        self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StaffProfile(Profile):
    user = models.OneToOneField('Staff', on_delete=models.CASCADE, related_name='staff_profile', verbose_name=_("User"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"Profile: {self.bio}"


@receiver(post_save, sender=Staff)
def create_or_update_staff_profile(sender, instance, created, **kwargs):
    if created:
        StaffProfile.objects.create(user=instance)
    else:
        instance.staff_profile.save()

# @receiver(post_save, sender=Staff)
# def save_staff_profile(sender, instance, **kwargs):
#     instance.staff_profile.save()
