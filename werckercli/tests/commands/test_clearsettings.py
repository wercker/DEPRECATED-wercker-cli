import mock

from werckercli.commands import clearsettings

from werckercli.tests import TestCase


class ClearSettingsTests(TestCase):

    def test_clear(self):
        # print dir(arg)

        home_path = "/werckercli/does_not_exist"

        with mock.patch(
            "os.path.isdir",
            mock.Mock(return_value=True)
        ):
            with mock.patch(
                "werckercli.paths.get_global_wercker_path",
                mock.Mock(return_value=home_path)
            ):
                with mock.patch(
                    "shutil.rmtree",
                    mock.Mock()
                ) as rmtree:
                    with mock.patch(
                        "clint.textui.puts",
                        mock.Mock()
                    ):
                        with mock.patch(
                            "werckercli.prompt.yn",
                            mock.Mock(return_value=True)
                        ):
                            my_clearsettings = reload(clearsettings)

                            my_clearsettings.clear_settings()
                            rmtree.assert_called_once_with(home_path)

    def test_NO_clear(self):
        # print dir(arg)

        home_path = "/werckercli/does_not_exist"

        with mock.patch(
            "os.path.isdir",
            mock.Mock(return_value=True)
        ):
            with mock.patch(
                "werckercli.paths.get_global_wercker_path",
                mock.Mock(return_value=home_path)
            ):
                with mock.patch(
                    "shutil.rmtree",
                    mock.Mock()
                ) as rmtree:
                    with mock.patch(
                        "clint.textui.puts",
                        mock.Mock()
                    ):
                        with mock.patch(
                            "werckercli.prompt.yn",
                            mock.Mock(return_value=False)
                        ):
                            my_clearsettings = reload(clearsettings)

                            my_clearsettings.clear_settings()
                            self.assertEqual(0, rmtree.call_count)
