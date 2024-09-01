
# Create your tests here.
from django.test import TestCase
from main_app.models import Lecturer, Subject

class SubjectLecturerTest(TestCase):
    def setUp(self):
        self.lecturer1 = Lecturer.objects.create(first_name="John", last_name="Doe")
        self.lecturer2 = Lecturer.objects.create(first_name="Jane", last_name="Smith")
        Subject.objects.create(name="Mathematics", code="MATH101", lecturer=self.lecturer1)
        Subject.objects.create(name="History", code="HIST101", lecturer=self.lecturer2)
        Subject.objects.create(name="Physics", code="PHYS101", lecturer=self.lecturer1)

    def test_subject_lecturers(self):
        math_subject = Subject.objects.get(name="Mathematics")
        history_subject = Subject.objects.get(name="History")
        physics_subject = Subject.objects.get(name="Physics")

        self.assertEqual(math_subject.lecturer, self.lecturer1)
        self.assertEqual(history_subject.lecturer, self.lecturer2)
        self.assertEqual(physics_subject.lecturer, self.lecturer1)