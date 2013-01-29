
from werckercli.decorators import login_required

from werckercli.tests import (
    BasicClientCase,
)


class LoginRequiredTests(BasicClientCase):
    template_name = "home-with-token"

    def test_valid_token(self):

        @login_required
        def nothing(valid_token=None):
            self.assertEqual(self.valid_token, valid_token)

        nothing()

    def test_return_value(self):

        @login_required
        def nothing(valid_token=None):

            return valid_token

        result = nothing()
        self.assertEqual(self.valid_token, result)
        # print result

    def test_argument_value(self):

        test_string = "test_string_1"

        @login_required
        def nothing(arg1, valid_token=None):
            self.assertEqual(arg1, test_string)

        nothing(test_string)
