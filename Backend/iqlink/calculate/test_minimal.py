from django.test import TestCase

class MinimalTests(TestCase):

    def test_basic(self):
        self.assertEqual(1 + 1, 2)

