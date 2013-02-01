import mock

from werckercli.tests import TestCase, VALID_TOKEN

from werckercli.commands import create


def test_decorator(f):
    def new_f(*args, **kwargs):
        return f(valid_token=VALID_TOKEN, *args, **kwargs)

    return new_f


class CreateTests(TestCase):

    @mock.patch("werckercli.decorators.login_required", test_decorator)
    def test_create(self):

        my_create = reload(create)
        result = my_create.create()

        print result

        # self.assertRaises(ValueError, unprotected_create)
