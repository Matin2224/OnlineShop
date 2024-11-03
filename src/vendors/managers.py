from accounts.managers import UserManager


class StaffManager(UserManager):
    def create_restaurant_manager(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return super().create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True, is_superuser=False)
