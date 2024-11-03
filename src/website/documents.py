# # shop/documents.py
#
# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from dashboard.models import ShopProduct, Shop
#
#
# @registry.register_document
# class ShopDocument(Document):
#     class Index:
#         name = 'dashboard'
#
#     class Django:
#         model = Shop
#         fields = ['name']
#
#
# # shop/documents.py
#
# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
#
# @registry.register_document
# class ShopProductDocument(Document):
#     # Indexing the name of the related Product model
#     product_name = fields.TextField(attr='product.name')  # Maps to Product's name field
#
#     class Index:
#         # Name of the Elasticsearch index
#         name = 'shop_products'
#
#     class Django:
#         model = ShopProduct
#         # Fields from ShopProduct model to be indexed
#         fields = [
#             'price',
#             'discount',
#             'discount_type',
#             'stock',
#             'average_rating',
#         ]
#
