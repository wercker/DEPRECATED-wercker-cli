import mock

from werckercli.tests import TestCase
from werckercli.commands.validate import validate

puts_path = "werckercli.commands.validate.puts"


class ValidationTests(TestCase):

    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value=None))
    def test_errors_when_no_git_repo_exists(self):
        with mock.patch(puts_path, mock.Mock()) as puts:
            validate()

            arg = SubstringMatcher(containing=
                                   "Could not find a git repository")
            puts.assert_called_with(arg)

    @mock.patch("os.path.exists", mock.Mock(return_value=False))
    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value="./"))
    def test_warns_when_wercker_json_not_exists(self):

        with mock.patch(puts_path, mock.Mock()) as puts:
            validate()

            puts.assert_called_with(SubstringMatcher(containing=
                                    "Could not find a wercker.json file"))

    @mock.patch("os.path.exists", mock.Mock(return_value=True))
    @mock.patch("os.path.getsize", mock.Mock(return_value=42))
    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value="./"))
    def test_puts_error_when_wercker_json_could_not_be_opened(self):
        e = IOError('foo')
        with mock.patch("os.open", mock.Mock(side_effect=e)) as open_file:
            with mock.patch(puts_path, mock.Mock()) as puts:
                validate()

                open_file.assert_called_once()
                puts.assert_called_with(SubstringMatcher(
                    containing="Error while reading wercker.json file:"))

    @mock.patch("os.path.exists", mock.Mock(return_value=True))
    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value="./"))
    @mock.patch("os.path.getsize", mock.Mock(return_value=0))
    def test_puts_error_when_wercker_json_is_empty(self):
        e = IOError('foo')
        with mock.patch("os.open", mock.Mock(side_effect=e)) as open_file:
            with mock.patch(puts_path, mock.Mock()) as puts:
                validate()

                open_file.assert_called_once()
                puts.assert_called_with(SubstringMatcher(containing=
                                        "wercker.json is found, but empty"))

    @mock.patch("os.open", mock.Mock(return_value=mock.MagicMock()))
    @mock.patch("os.path.exists", mock.Mock(return_value=True))
    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value="./"))
    @mock.patch("os.path.getsize", mock.Mock(return_value=42))
    def test_puts_error_when_wercker_json_is_not_valid(self):
        e = ValueError('foo')
        with mock.patch("json.load", mock.Mock(side_effect=e)) as json_load:
            with mock.patch(puts_path, mock.Mock()) as puts:
                validate()

                json_load.assert_called_once()
                puts.assert_called_with(SubstringMatcher(containing=
                                        "wercker.json is not valid json: "))

    @mock.patch("os.open", mock.Mock(return_value=mock.MagicMock()))
    @mock.patch("os.path.exists", mock.Mock(return_value=True))
    @mock.patch("werckercli.commands.validate.find_git_root",
                mock.Mock(return_value="./"))
    @mock.patch("os.path.getsize", mock.Mock(return_value=42))
    def test_puts_error_when_wercker_json_is_not_valid(self):
        with mock.patch("json.load", mock.Mock()) as json_load:
            with mock.patch(puts_path, mock.Mock()) as puts:
                validate()

                json_load.assert_called_once()
                puts.assert_called_with(SubstringMatcher(containing=
                                        "wercker.json is found and valid!"))


from string import lower


class SubstringMatcher():
    def __init__(self, containing):
        self.containing = lower(containing)

    def __eq__(self, other):
        return lower(other).find(self.containing) > -1

    def __unicode__(self):
        return 'a string containing "%s"' % self.containing

    def __str__(self):
        return unicode(self).encode('utf-8')

    __repr__ = __unicode__
