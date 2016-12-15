from didata_cli.cli import cli
from click.testing import CliRunner
import unittest
try:
    from unittest.mock import patch
except:
    from mock import patch
import os


@patch('didata_cli.cli.DimensionDataNodeDriver')
class DimensionDataCLITestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        os.environ["DIDATA_USER"] = 'fakeuser'
        os.environ["DIDATA_PASSWORD"] = 'fakepass'

    def test_image_help(self, node_client):
        result = self.runner.invoke(cli, ['image'], catch_exceptions=False)
        assert result.exit_code == 0
