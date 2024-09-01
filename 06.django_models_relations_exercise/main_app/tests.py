from django.test import TestCase

from caller import get_products_with_no_reviews
from main_app.models import Product, Review


class ProductReviewTestCase(TestCase):
    def setUp(self):
        """
        NOTE: Only for zero tests!
        """
        self.product1 = Product.objects.create(name='Laptop')
        self.product2 = Product.objects.create(name='Smartphone')
        self.product3 = Product.objects.create(name='Headphones')
        self.product4 = Product.objects.create(name='PlayStation 5')
        self.review1 = Review.objects.create(description='Great laptop!', rating=5, product=self.product1)
        self.review2 = Review.objects.create(description='The laptop is slow!', rating=2, product=self.product1)
        self.review3 = Review.objects.create(description='Awesome smartphone!', rating=5, product=self.product2)

    def test_zero_products_with_no_reviews(self):
        """
        Zero test for products with no reviews
        """
        products_with_no_reviews = get_products_with_no_reviews()
        self.assertEqual(products_with_no_reviews.count(), 2)
        self.assertEqual(products_with_no_reviews[0], self.product4)
        self.assertEqual(products_with_no_reviews[1], self.product3)