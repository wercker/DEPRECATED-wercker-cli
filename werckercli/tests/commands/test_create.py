import mock

from werckercli.tests import (
    DataSetTestCase,
    VALID_TOKEN

)

from werckercli.commands import create


def test_decorator(f):
    def new_f(*args, **kwargs):
        return f(valid_token=VALID_TOKEN, *args, **kwargs)

    return new_f


class CreateRemotesTests(DataSetTestCase):

    repo_name = "github-ssh"

    @mock.patch("werckercli.decorators.login_required", test_decorator)
    @mock.patch("__builtin__.raw_input", mock.Mock(return_value=""))
    @mock.patch("werckercli.cli.enter_url", mock.Mock(return_value=""))
    @mock.patch("clint.textui.puts", mock.Mock())
    def test_create(self):

        my_create = reload(create)
        result = my_create.create()
        self.assertEqual(result, "git@github.com:wercker/wercker-bruticus.git")

        # print result

        # self.assertRaises(ValueError, unprotected_create)


class CreatNoRemotesTests(DataSetTestCase):

    @mock.patch("werckercli.decorators.login_required", test_decorator)
    @mock.patch("__builtin__.raw_input", mock.Mock(return_value=""))
    @mock.patch("clint.textui.puts", mock.Mock())
    def test_create(self):

        my_create = reload(create)
        result = my_create.create()
        self.assertEqual(result, "git@github.com:wercker/wercker-bruticus.git")
