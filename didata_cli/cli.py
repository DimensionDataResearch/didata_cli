import click
import os
import sys

from libcloud.compute.drivers.dimensiondata import DimensionDataNodeDriver
from libcloud.backup.drivers.dimensiondata import DimensionDataBackupDriver

CONTEXT_SETTINGS = {
    'auto_envvar_prefix': 'MCP'
}
DEFAULT_OUTPUT_TYPE = 'pretty'


class DiDataCLIClient(object):
    def __init__(self):
        self.node = None
        self.backup = None
        self.verbose = False

    def init_client(self, user, password, region):
        self.node = DimensionDataNodeDriver(user, password, region=region)
        self.backup = DimensionDataBackupDriver(user, password, region=region)

pass_client = click.make_pass_decorator(DiDataCLIClient, ensure=True)
cmd_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'commands'
))


class DiDataCLI(click.MultiCommand):

    def list_commands(self, ctx):
        commands = [
            filename[4:-3]
            for filename in os.listdir(cmd_folder)
            if filename.endswith('.py') and filename.startswith('cmd_')
        ]
        commands.sort()

        return commands

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')

            module = __import__(
                name='didata_cli.commands.cmd_' + name,
                globals=None,
                locals=None,
                fromlist=['cli']
            )
        except ImportError:
            return  # AF: Shouldn't just swallow this error; a module syntax error would be reported as command not found.

        return module.cli


@click.command(cls=DiDataCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True)
@click.option('--user', allow_from_autoenv=True)
@click.option('--password', allow_from_autoenv=True)
@click.option('--region', allow_from_autoenv=True)
@click.option('--output-type', default=DEFAULT_OUTPUT_TYPE)
@pass_client
def cli(client, verbose, user, password, region, output_type):
    """An interface into the Dimension Data Cloud"""

    # TODO: Fall back to credentials from "~/.dimensiondata"

    if not user:
        click.echo(
            'Username must be specified via --user option or MCP_USER environment variable.',
            err=True
        )

        exit(1)

    if not password:
        click.echo(
            'Password must be specified via --password option or MCP_PASSWORD environment variable.',
            err=True
        )

        exit(1)

    if not region:
        click.echo(
            'Target region must be specified via --region option or MCP_REGION environment variable.',
            err=True
        )

        exit(1)

    client.init_client(user, password, region)
    client.output_type = output_type
    if verbose:
        click.echo('Verbose mode enabled')
