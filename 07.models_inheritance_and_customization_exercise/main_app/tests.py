from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from main_app.models import Student, StudentIDField


class StudentModelTestCase(TestCase):
    def test_zero_float_value(self):
        """
        Zero Test creating a Student object with a float student ID.
        """
        student = Student(name='Alice', student_id=45.23)
        student.full_clean()
        student.save()
        student.refresh_from_db()
        self.assertIsInstance(student.student_id, int)
        self.assertEqual(student.student_id, 45)