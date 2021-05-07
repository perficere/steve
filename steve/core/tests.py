from django.test import TestCase


class MetaTestCase(TestCase):
    def setUp(self):
        self.a_true_statement = True

    def test_assert_true(self):
        """
        Tests are working correctly.
        """
        self.assertTrue(self.a_true_statement)
