# from django.test import TestCase
#
# # Create your tests here.
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Address, Profile
# import jdatetime
#
#
#
#
# class AddressModelTest(TestCase):
#     def test_create_address(self):
#         address = Address.objects.create(
#             street="خیابان انقلاب",
#             city="تهران",
#             state="تهران",
#             zipcode="1234567890"
#         )
#
#         self.assertEqual(str(address), "خیابان: خیابان انقلاب، شهر: تهران، استان: تهران، کد پستی: 1234567890")
#         self.assertEqual(address.zipcode, "1234567890")
#         self.assertEqual(address.city, "تهران")
#
# # class UserModelTest(TestCase):
# #
# #     def setUp(self):
# #         self.user = User.objects.create_user(
# #             email="tests@example.com",
# #             phone="09123456789",
# #             password="testpassword123",
# #             birthdate="2000-01-01"
# #         )
# #
# #     def test_create_user(self):
# #         self.assertEqual(self.user.email, "tests@example.com")
# #         self.assertEqual(self.user.phone, "09123456789")
# #         self.assertFalse(self.user.is_superuser)
# #         self.assertTrue(self.user.check_password("testpassword123"))
# #
# #     def test_persian_date_joined(self):
# #         persian_date = jdatetime.date.fromgregorian(date=self.user.date_joined).strftime('%Y-%m-%d %H:%M:%S')
# #         self.assertEqual(self.user.persian_date_joined(), persian_date)
# #
# #     def test_persian_birthdate(self):
# #         persian_birthdate = jdatetime.date.fromgregorian(date=self.user.birthdate).strftime('%Y-%m-%d')
# #         self.assertEqual(self.user.persian_birthdate(), persian_birthdate)
# #
# #     def test_string_representation(self):
# #         self.assertEqual(str(self.user), self.user.get_full_name())
#
# # class ProfileModelTest(TestCase):
# #
# #     def setUp(self):
# #         self.user = User.objects.create_user(
# #             email="profiletest@example.com",
# #             phone="09123456780",
# #             password="testpassword123"
# #         )
# #         self.profile = Profile.objects.create(
# #             user=self.user,
# #             bio="This is a tests bio."
# #         )
# #
# #     def test_create_profile(self):
# #         self.assertEqual(str(self.profile), f"Profile of {self.user.email}")
# #         self.assertEqual(self.profile.bio, "This is a tests bio.")
# #         self.assertEqual(self.profile.user.email, "profiletest@example.com")
# #         self.assertEqual(self.profile.profile_image.name, "default.jpg")
