from didata_cli.cli import cli
from click.testing import CliRunner
import unittest
try:
    from unittest.mock import patch
except:
    from mock import patch
import os
from tests.utils import load_dd_obj
from libcloud.common.dimensiondata import DimensionDataAPIException


@patch('didata_cli.cli.DimensionDataNodeDriver')
class DimensionDataCLITestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        os.environ["DIDATA_USER"] = 'fakeuser'
        os.environ["DIDATA_PASSWORD"] = 'fakepass'

    def test_network_help(self, node_client):
        result = self.runner.invoke(cli, ['network'], catch_exceptions=False)
        assert result.exit_code == 0

    def test_vlan_list(self, node_client):
        node_client.return_value.ex_list_vlans.return_value = load_dd_obj('vlan_list.json')
        result = self.runner.invoke(cli, ['network', 'list_vlans'])
        self.assertTrue('ID: 56389c71-cc03-4e7a-a72f-cc219f0649c8' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_vlan_list_with_network_domain_id(self, node_client):
        node_client.return_value.ex_list_vlans.return_value = load_dd_obj('vlan_list.json')
        result = self.runner.invoke(cli, ['network', 'list_vlans', '--networkDomainId',
                                          '4b58cd5-4968-4b84-ac4c-007a5c1dd6f5'])
        self.assertTrue('ID: 56389c71-cc03-4e7a-a72f-cc219f0649c8' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_vlan_list_APIException(self, node_client):
        node_client.return_value.ex_list_vlans.side_effect = DimensionDataAPIException(
            code='REASON 541', msg='Unable to list vlans', driver=None)
        result = self.runner.invoke(cli, ['network', 'list_vlans'])
        self.assertTrue('REASON 541' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_create_vlan(self, node_client):
        node_client.return_value.ex_create_vlan.return_value = load_dd_obj('vlan.json')
        result = self.runner.invoke(cli, ['network', 'create_vlan',
                                          '--networkDomainId', '423c4386-87b4-43c4-9604-88ae237bfc7f',
                                          '--name', 'overlap_vlan',
                                          '--baseIpv4Address', '10.192.238.0'])
        self.assertTrue('eee454f4-562a-4b23-ad57-4cb8b034c8c9' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_create_vlan_APIException(self, node_client):
        node_client.return_value.ex_create_vlan.side_effect = DimensionDataAPIException(
            code='REASON 540', msg='Unable to create vlan', driver=None)
        result = self.runner.invoke(cli, ['network', 'create_vlan',
                                          '--networkDomainId', '423c4386-87b4-43c4-9604-88ae237bfc7f',
                                          '--name', 'overlap_vlan',
                                          '--baseIpv4Address', '10.192.238.0'])
        self.assertTrue('REASON 540' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_delete_vlan(self, node_client):
        node_client.return_value.ex_delete_vlan.return_value = True
        result = self.runner.invoke(cli, ['network', 'delete_vlan',
                                          '--vlanId', 'eee454f4-562a-4b23-ad57-4cb8b034c8c9'])
        self.assertTrue('eee454f4-562a-4b23-ad57-4cb8b034c8c9' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_delete_vlan_APIException(self, node_client):
        node_client.return_value.ex_delete_vlan.side_effect = DimensionDataAPIException(
            code='REASON 542', msg='Unable to delete vlan', driver=None)
        result = self.runner.invoke(cli, ['network', 'delete_vlan',
                                          '--vlanId', 'eee454f4-562a-4b23-ad57-4cb8b034c8c9'])
        self.assertTrue('REASON 542' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_network_domain_list(self, node_client):
        node_client.return_value.ex_list_network_domains.return_value = load_dd_obj('network_domain_list.json')
        result = self.runner.invoke(cli, ['network', 'list_network_domains'])
        self.assertTrue('ID: a4b58cd5-4968-4b84-ac4c-007a5c1dd6f5' in result.output)
        self.assertTrue('ID: 75b72ac5-0f3e-4c44-96f1-61b6aa5cae43' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_network_domain_list_APIException(self, node_client):
        node_client.return_value.ex_list_network_domains.side_effect = DimensionDataAPIException(
            code='REASON 543', msg='Unable to list network domains', driver=None)
        result = self.runner.invoke(cli, ['network', 'list_network_domains'])
        self.assertTrue('REASON 543' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_create_network_domain(self, node_client):
        node_client.return_value.ex_create_network_domain.return_value = load_dd_obj('network_domain.json')
        result = self.runner.invoke(cli, ['network', 'create_network_domain',
                                          '--name', 'fake_network_domain',
                                          '--servicePlan', 'ESSENTIALS',
                                          '--datacenterId', 'NA9'])
        self.assertTrue('Network Domain fake_network_domain created' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_create_network_domain_APIException(self, node_client):
        node_client.return_value.ex_create_network_domain.side_effect = DimensionDataAPIException(
            code='REASON 544', msg='Unable to create network domain', driver=None)
        result = self.runner.invoke(cli, ['network', 'create_network_domain',
                                          '--name', 'fake_network_domain',
                                          '--servicePlan', 'ESSENTIALS',
                                          '--datacenterId', 'NA9'])
        self.assertTrue('REASON 544' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_delete_network_domain(self, node_client):
        node_client.return_value.ex_delete_network_domain.return_value = True
        result = self.runner.invoke(cli, ['network', 'delete_network_domain',
                                          '--networkDomainId', 'fake_network_domain'])
        self.assertTrue('Network Domain fake_network_domain deleted' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_delete_network_domain_APIException(self, node_client):
        node_client.return_value.ex_delete_network_domain.side_effect = DimensionDataAPIException(
            code='REASON 545', msg='Unable to delete network domain', driver=None)
        result = self.runner.invoke(cli, ['network', 'delete_network_domain',
                                          '--networkDomainId', 'fake_network_domain'])
        self.assertTrue('REASON 545' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_network_list(self, node_client):
        node_client.return_value.ex_list_networks.return_value = load_dd_obj('network_list.json')
        result = self.runner.invoke(cli, ['network', 'list_networks'])
        self.assertTrue('ID: 629aac56-0cea-11e4-b29c-001517c4643e' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_network_list_APIException(self, node_client):
        node_client.return_value.ex_list_networks.side_effect = DimensionDataAPIException(
            code='REASON 548', msg='Unable to list networks', driver=None)
        result = self.runner.invoke(cli, ['network', 'list_networks'])
        self.assertTrue('REASON 548' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_create_network(self, node_client):
        node_client.return_value.ex_create_network.return_value = load_dd_obj('network.json')
        result = self.runner.invoke(cli, ['network', 'create_network',
                                          '--name', 'fake_network',
                                          '--servicePlan', 'ESSENTIALS',
                                          '--datacenterId', 'NA9'])
        self.assertTrue('Network fake_network created' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_create_network_APIException(self, node_client):
        node_client.return_value.ex_create_network.side_effect = DimensionDataAPIException(
            code='REASON 546', msg='Unable to create network', driver=None)
        result = self.runner.invoke(cli, ['network', 'create_network',
                                          '--name', 'fake_network',
                                          '--servicePlan', 'ESSENTIALS',
                                          '--datacenterId', 'NA9'])
        self.assertTrue('REASON 546' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_delete_network(self, node_client):
        node_client.return_value.ex_delete_network.return_value = True
        result = self.runner.invoke(cli, ['network', 'delete_network',
                                          '--networkId', 'fake_network'])
        self.assertTrue('Network fake_network deleted' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_delete_network_APIException(self, node_client):
        node_client.return_value.ex_delete_network.side_effect = DimensionDataAPIException(
            code='REASON 547', msg='Unable to delete network', driver=None)
        result = self.runner.invoke(cli, ['network', 'delete_network',
                                          '--networkId', 'fake_network'])
        self.assertTrue('REASON 547' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_create_firewall_rule(self, node_client):
        node_client.return_value.ex_get_network_domain.return_value = load_dd_obj('network_domain.json')
        node_client.return_value.ex_create_firewall_rule.return_value = True
        result = self.runner.invoke(cli, ['network', 'create_firewall_rule',
                                          '--name', 'my_fake_rule',
                                          '--networkDomainId', 'fake_network_domain',
                                          '--ipVersion', 'IPV4',
                                          '--action', 'DROP',
                                          '--protocol', 'TCP',
                                          '--sourceIP', 'ANY',
                                          '--sourceStartPort', 'ANY',
                                          '--destinationIP', '10.1.1.15',
                                          '--destinationStartPort', 'ANY',
                                          '--position', 'LAST'])
        self.assertTrue('Firewall rule my_fake_rule created' in result.output)
        self.assertEqual(result.exit_code, 0)

    def test_create_firewall_rule_APIException(self, node_client):
        node_client.return_value.ex_create_firewall_rule.side_effect = DimensionDataAPIException(
            code='REASON 549', msg='Unable to create firewall rule', driver=None)
        result = self.runner.invoke(cli, ['network', 'create_firewall_rule',
                                          '--name', 'my_fake_rule',
                                          '--networkDomainId', 'fake_network_domain',
                                          '--ipVersion', 'IPV4',
                                          '--action', 'DROP',
                                          '--protocol', 'TCP',
                                          '--sourceIP', 'ANY',
                                          '--sourceStartPort', 'ANY',
                                          '--destinationIP', '10.1.1.15',
                                          '--destinationStartPort', 'ANY',
                                          '--position', 'LAST'])
        self.assertTrue('REASON 549' in result.output)
        self.assertTrue(result.exit_code == 1)

    def test_list_firewall_rule(self, node_client):
        node_client.return_value.ex_get_network_domain.return_value = load_dd_obj('network_domain.json')
        node_client.return_value.ex_list_firewall_rules.return_value = load_dd_obj('firewall_rule_list.json')
        result = self.runner.invoke(cli, ['network', 'list_firewall_rules', '--networkDomainId', 'fake_network_domain'])
        print(result.output)
        self.assertTrue('Name: CCDEFAULT.BlockOutboundMailIPv4Secure' in result.output)
        self.assertEqual(result.exit_code, 0)
