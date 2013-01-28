from werckercli.tests import (
    TestCase
)

from werckercli import cli


class PrintIntroTtests(TestCase):

    def test_get_intro(self):

        result = cli.get_intro()

        self.assertTrue(result.find('wercker') != -1)


class GetParserTests(TestCase):

    def test_returns_parser(self):

        from argparse import ArgumentParser

        result = cli.get_parser()

        self.assertTrue(type(result) == ArgumentParser)
