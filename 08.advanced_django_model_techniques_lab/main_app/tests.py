from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from main_app.models import Restaurant, Menu
from django.core.exceptions import ValidationError


class MenuModelTest(TestCase):
    def setUp(self):
        # Create a sample restaurant for testing
        self.restaurant = Restaurant.objects.create(
            name="The Delicious Bistro",
            location="123 Main St.",
            rating=4.5,
        )

    def test_valid_menu(self):
        valid_menu = Menu(
            name="Menu at The Delicious Bistro",
            description="** Appetizers: **\nSpinach and Artichoke Dip\n** Main Course: **\nGrilled Salmon\n** Desserts: **\nChocolate Fondue",
            restaurant=self.restaurant,
        )

        try:
            valid_menu.full_clean()
            valid_menu.save()
            self.assertEqual(Menu.objects.count(), 1)
        except ValidationError as e:
            self.fail(f"Validation Error: {e}")

    def test_invalid_menu(self):
        invalid_menu = Menu(
            name="Incomplete Menu",
            description="** Appetizers: **\nSpinach and Artichoke Dip",
            restaurant=self.restaurant,
        )

        with self.assertRaises(ValidationError) as context:
            invalid_menu.full_clean()

        # Assert the specific validation error messages
        self.assertEqual(
            context.exception.message_dict["description"][0],
            'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".'
        )
