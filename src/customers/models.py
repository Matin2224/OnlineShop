from django.utils.translation import gettext_lazy as _

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, Address, Profile
from customers.managers import CustomerManager


class Customer(User):
    objects = CustomerManager()
    address = models.ManyToManyField(Address, related_name='customer_address', verbose_name=_("Address"))

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def save(self, *args, **kwargs):
        if not self.id:
            self.is_staff = False
            self.is_superuser = False
            self.is_customer = True
        return super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}"


class CustomerProfile(Profile):
    user = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='customer_profile',
                                verbose_name=_("User"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


@receiver(post_save, sender=Customer)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)
    else:
        instance.customer_profile.save()

# @receiver(post_save, sender=Customer)
# def save_customer_profile(sender, instance, **kwargs):
#     instance.customer_profile.save()
