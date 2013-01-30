from werckercli.tests import TestCase

from werckercli.commands.create import unprotected_create


class CreateTests(TestCase):

    def test_create(self):
        self.assertRaises(ValueError, unprotected_create)
