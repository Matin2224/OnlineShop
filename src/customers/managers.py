from accounts.managers import UserManager


class CustomerManager(UserManager):
    def create_customer(self, email, password, **extra_fields):
        extra_fields.setdefault('is_customer', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return super().create_user(email, password, **extra_fields)

