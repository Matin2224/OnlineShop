import jdatetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from . managers import UserManager


class Address(models.Model):
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    street = models.CharField(max_length=100, verbose_name=_("Street"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    state = models.CharField(max_length=50, verbose_name=_("State"))
    zipcode = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
        verbose_name=_("Zip Code")
    )

    def __str__(self):
        return f"خیابان: {self.street}, شهر: {self.city}, استان: {self.state}, کد پستی: {self.zipcode}"


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name=_("Email address"), unique=True)
    phone_regex = RegexValidator(
        regex=r'^(09)\d{9}$',
        message=_("Phone number must be entered in the format: '09123456789'.")
    )
    phone = models.CharField(verbose_name=_('Phone'), max_length=11, unique=True, validators=[phone_regex])
    birthdate = models.DateField(verbose_name=_('Birth Date'), null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def persian_date_joined(self):
        persian_date = jdatetime.date.fromgregorian(date=self.date_joined).strftime('%Y-%m-%d %H:%M:%S')
        return persian_date

    def persian_birthdate(self):
        persian_birthdate = jdatetime.date.fromgregorian(date=self.date_joined).strftime('%Y-%m-%d')
        return persian_birthdate

    def __str__(self):
        return self.get_full_name()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',verbose_name=_('User'))
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name=_("Profile Image"),default='default.jpg')

    class Meta:
        abstract = True

    def __str__(self):
        return "Profile of %(email)s" % {'email': self.user.email}

