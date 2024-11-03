from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from website.models import Category, Product, Image


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")
        self.assertIsNone(self.category.parents)

    def test_category_slug_generation(self):
        new_category = Category.objects.create(name="Electronics")
        self.assertNotEqual(new_category.slug, "electronics")
        self.assertTrue(new_category.slug.startswith("electronics-"))

    def test_category_with_parent(self):
        parent_category = Category.objects.create(name="Parent Category")
        child_category = Category.objects.create(name="Child Category", parents=parent_category)
        self.assertEqual(child_category.parents, parent_category)
        self.assertEqual(parent_category.parent_categories.first(), child_category)

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone", category=self.category, properties="Brand: XYZ, Model: ABC"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.slug, "smartphone")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.properties, "Brand: XYZ, Model: ABC")
        self.assertEqual(self.product.average_rating, 1.0)

    def test_product_slug_generation(self):
        new_product = Product.objects.create(name="Smartphone", category=self.category)
        self.assertNotEqual(new_product.slug, "smartphone")
        self.assertTrue(new_product.slug.startswith("smartphone-"))

    def test_update_average_rating(self):
        self.product.rating_count = 5
        self.product.sum_rating = 20
        self.product.update_average_rating()
        self.assertEqual(self.product.average_rating, 4.0)


class ImageModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category)
        self.content_type = ContentType.objects.get_for_model(self.product)
        self.image = Image.objects.create(
            content_type=self.content_type, object_id=self.product.id, image="images/test.jpg"
        )

    def test_image_creation(self):
        self.assertEqual(self.image.image, "images/test.jpg")
        self.assertEqual(self.image.content_type, self.content_type)
        self.assertEqual(self.image.object_id, self.product.id)
        self.assertEqual(self.image.content_object, self.product)

    def test_image_str(self):
        self.assertEqual(str(self.image), f"Image for {self.product}")
