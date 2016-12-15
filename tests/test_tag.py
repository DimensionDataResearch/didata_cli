from didata_cli.cli import cli
from click.testing import CliRunner
from libcloud.common.dimensiondata import DimensionDataAPIException
from tests.utils import load_dd_obj
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

    def test_tag_help(self, node_client):
        result = self.runner.invoke(cli, ['tag'], catch_exceptions=False)
        assert result.exit_code == 0

    def test_tag_create_key(self, node_client):
        node_client.return_value.ex_create_tag_key.return_value = True
        result = self.runner.invoke(cli,
                                    ['tag', 'create_key',
                                     '--name', 'faketagkey'])
        self.assertTrue('created' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_create_key_return_False(self, node_client):
        node_client.return_value.ex_create_tag_key.return_value = False
        result = self.runner.invoke(cli,
                                    ['tag', 'create_key',
                                     '--name', 'faketagkey'])
        self.assertTrue('Error when creating' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_create_key_APIException(self, node_client):
        node_client.return_value.ex_create_tag_key.side_effect = DimensionDataAPIException(
            code='REASON 501', msg='Cannot create tag key', driver=None)
        result = self.runner.invoke(cli,
                                    ['tag', 'create_key',
                                     '--name', 'faketagkey'])
        self.assertTrue('REASON 501' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_modify_key(self, node_client):
        node_client.return_value.ex_modify_tag_key.return_value = True
        result = self.runner.invoke(cli,
                                    ['tag', 'modify_key',
                                     '--tagKeyId', 'faketagkey', '--name', 'newtagkeyname'])
        self.assertTrue('modified' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_modify_key_return_False(self, node_client):
        node_client.return_value.ex_modify_tag_key.return_value = False
        result = self.runner.invoke(cli,
                                    ['tag', 'modify_key',
                                     '--tagKeyId', 'faketagkey', '--name', 'newtagkeyname'])
        self.assertTrue('Error when modifying' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_modify_key_APIException(self, node_client):
        node_client.return_value.ex_modify_tag_key.side_effect = DimensionDataAPIException(
            code='REASON 502', msg='Cannot modify tag key', driver=None)
        result = self.runner.invoke(cli,
                                    ['tag', 'modify_key',
                                     '--tagKeyId', 'faketagkey', '--name', 'newtagkeyname'])
        self.assertTrue('REASON 502' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_remove_key(self, node_client):
        node_client.return_value.ex_remove_tag_key.return_value = True
        result = self.runner.invoke(cli,
                                    ['tag', 'remove_key',
                                     '--tagKeyId', 'faketagkey'])
        self.assertTrue('removed' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_remove_key_return_False(self, node_client):
        node_client.return_value.ex_remove_tag_key.return_value = False
        result = self.runner.invoke(cli,
                                    ['tag', 'remove_key',
                                     '--tagKeyId', 'faketagkey'])
        self.assertTrue('Error when removing' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_remove_key_APIException(self, node_client):
        node_client.return_value.ex_remove_tag_key.side_effect = DimensionDataAPIException(
            code='REASON 503', msg='Cannot remove tag key', driver=None)
        result = self.runner.invoke(cli,
                                    ['tag', 'remove_key',
                                     '--tagKeyId', 'faketagkey'])
        self.assertTrue('REASON 503' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_list_keys(self, node_client):
        node_client.return_value.ex_list_tag_keys.return_value = load_dd_obj('tag_keys.json')
        result = self.runner.invoke(cli,
                                    ['tag', 'list_keys'])
        self.assertTrue('Name: Target' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_list_keys_query(self, node_client):
        node_client.return_value.ex_list_tag_keys.return_value = load_dd_obj('tag_keys.json')
        result = self.runner.invoke(cli, ['tag', 'list_keys', '--query', "ReturnCount:1|ReturnKeys:Name"])
        self.assertEqual(result.exit_code, 0)
        output = os.linesep.join([s for s in result.output.splitlines() if s])
        self.assertEqual(output, 'Name: AaronTestModified')

    def test_tag_list_keys_empty(self, node_client):
        node_client.return_value.ex_list_tag_keys.return_value = load_dd_obj('tag_key_list_empty.json')
        result = self.runner.invoke(cli,
                                    ['tag', 'list_keys'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('No tags found', result.output)

    def test_tag_apply_server(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_apply_tag_to_asset.return_value = True
        result = self.runner.invoke(cli,
                                    ['tag', 'apply', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('Tag applied' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_apply_server_return_FALSE(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_apply_tag_to_asset.return_value = False
        result = self.runner.invoke(cli,
                                    ['tag', 'apply', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('Error when applying' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_apply_server_APIException(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_apply_tag_to_asset.side_effect = DimensionDataAPIException(
            code='REASON 503', msg='Cannot apply tag', driver=None)
        result = self.runner.invoke(cli,
                                    ['tag', 'apply', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('REASON 503' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_remove_server(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_remove_tag_from_asset.return_value = True
        result = self.runner.invoke(cli,
                                    ['tag', 'remove', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('Tag removed' in result.output)
        self.assertTrue(result.exit_code == 0)

    def test_tag_remove_server_return_FALSE(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_remove_tag_from_asset.return_value = False
        result = self.runner.invoke(cli,
                                    ['tag', 'remove', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('Error when removing' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_tag_remove_server_APIException(self, node_client):
        node_client.return_value.ex_get_node_by_id.return_value = load_dd_obj('node.json')
        node_client.return_value.ex_remove_tag_from_asset.side_effect = DimensionDataAPIException(
            code='REASON 504', msg='Cannot remove tag', driver=None)
        result = self.runner.invoke(cli,
                                    ['tag', 'remove', '--id', 'fakeserverid',
                                     '--assetType', 'SERVER',
                                     '--tagKeyName', 'faketagkeyname'])
        self.assertTrue('REASON 504' in result.output)
        self.assertTrue(result.exit_code == 1)
