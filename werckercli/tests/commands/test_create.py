import os
import mock

from werckercli.tests import (
    DataSetTestCase,
    VALID_TOKEN

)

from werckercli.commands import create


# def test_decorator(f):
#     def new_f(*args, **kwargs):
#         return f(valid_token=VALID_TOKEN, *args, **kwargs)

#     return new_f


# class CreateRemotesTests(DataSetTestCase):

#     repo_name = "github-ssh"

#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value=""))
#     @mock.patch("werckercli.cli.enter_url", mock.Mock(return_value=""))
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create_default(self):

#         my_create = reload(create)
#         result = my_create.create(
#             path=os.path.join(
#                 self.folder,
#                 self.repo_name,
#                 self.get_git_folder()
#             )
#         )
#         self.assertEqual(
#             result,
#             "git@github.com:wercker/wercker-cli.git"
#         )

#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value="1"))
#     @mock.patch("werckercli.cli.enter_url", mock.Mock(return_value=""))
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create_1(self):

#         my_create = reload(create)
#         result = my_create.create(
#             path=os.path.join(
#                 self.folder,
#                 self.repo_name,
#                 self.get_git_folder()
#             )
#         )
#         self.assertEqual(
#             result,
#             "git@github.com:wercker/wercker-cli.git"
#         )

#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value="2"))
#     @mock.patch(
#         "werckercli.cli.enter_url",
#         mock.Mock(
#             return_value="VALID_URL"
#         )
#     )
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create_2(self):

#         my_create = reload(create)
#         result = my_create.create(
#             path=os.path.join(
#                 self.folder,
#                 self.repo_name,
#                 self.get_git_folder()
#             )
#         )
#         self.assertEqual(
#             result,
#             "VALID_URL"
#         )
        # print result

        # self.assertRaises(ValueError, unprotected_create)


# VALID_OTHER_URL = "git@bitbucket.org:flenter:django_scm_deploytools"

# class CreatNoRemotesTests(DataSetTestCase):

#     repo_name="github-ssh"

#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value=""))
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create(self):

#         my_create = reload(create)
#         result = my_create.create()
        # self.assertEqual(
        #     result,
        #     "git@github.com:wercker/wercker-cli.git"
        # )

#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value="1"))
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create(self):

#         my_create = reload(create)
#         result = my_create.create()
        # self.assertEqual(
        #     result,
        #     "git@github.com:wercker/wercker-cli.git"
        # )


#     @mock.patch("werckercli.decorators.login_required", test_decorator)
#     @mock.patch("__builtin__.raw_input", mock.Mock(return_value="2"))
    # @mock.patch(
    #     "werckercli.cli.enter_url",
    #     mock.Mock(return_value=VALID_OTHER_URL)
    # )
#     @mock.patch("clint.textui.puts", mock.Mock())
#     def test_create(self):

#         my_create = reload(create)
#         result = my_create.create()
#         self.assertEqual(result, VALID_OTHER_URL)
