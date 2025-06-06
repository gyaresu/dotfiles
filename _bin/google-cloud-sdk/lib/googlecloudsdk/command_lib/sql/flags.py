# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common flags for some of the SQL commands.

Flags are specified with functions that take in a single argument, the parser,
and add the newly constructed flag to that parser.

Example:

def AddFlagName(parser):
  parser.add_argument(
    '--flag-name',
    ... // Other flag details.
  )
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from __future__ import unicode_literals
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.util import completers


_IP_ADDRESS_PART = r'(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})'  # Match decimal 0-255
_CIDR_PREFIX_PART = r'([0-9]|[1-2][0-9]|3[0-2])'  # Match decimal 0-32
# Matches either IPv4 range in CIDR notation or a naked IPv4 address.
_CIDR_REGEX = r'{addr_part}(\.{addr_part}){{3}}(\/{prefix_part})?$'.format(
    addr_part=_IP_ADDRESS_PART, prefix_part=_CIDR_PREFIX_PART)


class DatabaseCompleter(completers.ListCommandCompleter):

  def __init__(self, **kwargs):
    super(DatabaseCompleter, self).__init__(
        collection='sql.databases',
        api_version='v1beta4',
        list_command='sql databases list --uri',
        flags=['instance'],
        **kwargs)


class InstanceCompleter(completers.ListCommandCompleter):

  def __init__(self, **kwargs):
    super(InstanceCompleter, self).__init__(
        collection='sql.instances',
        list_command='sql instances list --uri',
        **kwargs)


class UserCompleter(completers.ListCommandCompleter):

  def __init__(self, **kwargs):
    super(UserCompleter, self).__init__(
        collection=None,  # TODO(b/62961917): Should be 'sql.users',
        api_version='v1beta4',
        list_command='sql users list --flatten=name[] --format=disable',
        flags=['instance'],
        **kwargs)


def AddInstance(parser):
  parser.add_argument(
      '--instance',
      '-i',
      required=True,
      completer=InstanceCompleter,
      help='Cloud SQL instance ID.')


def AddInstanceArgument(parser):
  """Add the 'instance' argument to the parser."""
  parser.add_argument(
      'instance',
      completer=InstanceCompleter,
      help='Cloud SQL instance ID.')


# Currently, 10230 is the max storage size one can set, and 10 is the minimum.
def AddInstanceResizeLimit(parser):
  parser.add_argument(
      '--storage-auto-increase-limit',
      type=arg_parsers.BoundedInt(10, 10230, unlimited=True),
      help='Allows you to set a maximum storage capacity, in GB. Automatic '
      'increases to your capacity will stop once this limit has been reached. '
      'Default capacity is *unlimited*.')


def AddUsername(parser):
  parser.add_argument(
      'username',
      completer=UserCompleter,
      help='Cloud SQL username.')


def AddHost(parser):
  parser.add_argument('host', help='Cloud SQL user\'s host.')


def AddAvailabilityType(parser):
  """Add the '--availability-type' flag to the parser."""
  availabilty_type_flag = base.ChoiceArgument(
      '--availability-type',
      required=False,
      choices={
          'regional': 'Provides high availability and is recommended for '
                      'production instances; instance automatically fails over '
                      'to another zone within your selected region.',
          'zonal': 'Provides no failover capability. This is the default.'
      },
      help_str=('Specifies level of availability. Only applies to PostgreSQL '
                'instances.'))
  availabilty_type_flag.AddToParser(parser)


def AddPassword(parser):
  parser.add_argument(
      '--password',
      help='Cloud SQL user\'s password.')


def AddPromptForPassword(parser):
  parser.add_argument(
      '--prompt-for-password',
      action='store_true',
      help=('Prompt for the Cloud SQL user\'s password with character echo '
            'disabled. The password is all typed characters up to but not '
            'including the RETURN or ENTER key.'))


# Instance create and patch flags


def AddActivationPolicy(parser):
  parser.add_argument(
      '--activation-policy',
      required=False,
      choices=['ALWAYS', 'NEVER', 'ON_DEMAND'],
      default=None,
      help=('The activation policy for this instance. This specifies when '
            'the instance should be activated and is applicable only when '
            'the instance state is RUNNABLE. The default is ON_DEMAND. '
            'More information on activation policies can be found here: '
            'https://cloud.google.com/sql/faq#activation_policy'))


def AddAssignIp(parser, show_negated_in_help=False):
  kwargs = _GetKwargsForBoolFlag(show_negated_in_help)
  parser.add_argument(
      '--assign-ip',
      help='The instance must be assigned an IP address.', **kwargs)


def AddAuthorizedGAEApps(parser):
  parser.add_argument(
      '--authorized-gae-apps',
      type=arg_parsers.ArgList(min_length=1),
      metavar='APP',
      required=False,
      help=('First Generation instances only. List of IDs for App Engine '
            'applications running in the Standard environment that '
            'can access this instance.'))


def AddAuthorizedNetworks(parser):
  cidr_validator = arg_parsers.RegexpValidator(
      _CIDR_REGEX, ('Must be specified in CIDR notation, also known as '
                    '\'slash\' notation (e.g. 192.168.100.0/24).'))
  parser.add_argument(
      '--authorized-networks',
      type=arg_parsers.ArgList(min_length=1, element_type=cidr_validator),
      metavar='NETWORK',
      required=False,
      default=[],
      help=('The list of external networks that are allowed to connect to '
            'the instance. Specified in CIDR notation, also known as '
            '\'slash\' notation (e.g. 192.168.100.0/24).'))


def AddBackupStartTime(parser):
  parser.add_argument(
      '--backup-start-time',
      required=False,
      help=('The start time of daily backups, specified in the 24 hour '
            'format - HH:MM, in the UTC timezone.'))


def AddDatabaseFlags(parser):
  parser.add_argument(
      '--database-flags',
      type=arg_parsers.ArgDict(min_length=1),
      metavar='FLAG=VALUE',
      required=False,
      help=('A comma-separated list of database flags to set on the '
            'instance. Use an equals sign to separate flag name and value. '
            'Flags without values, like skip_grant_tables, can be written '
            'out without a value after, e.g., `skip_grant_tables=`. Use '
            'on/off for booleans. View the Instance Resource API for allowed '
            'flags. (e.g., `--database-flags max_allowed_packet=55555,'
            'skip_grant_tables=,log_output=1`)'))


def AddCPU(parser):
  parser.add_argument(
      '--cpu',
      type=int,
      required=False,
      help=('A whole number value indicating how many cores are desired in '
            'the machine. Both --cpu and --memory must be specified if a '
            'custom machine type is desired, and the --tier flag must be '
            'omitted.'))


def _GetKwargsForBoolFlag(show_negated_in_help):
  if show_negated_in_help:
    return {
        'action': arg_parsers.StoreTrueFalseAction,
    }
  else:
    return {
        'action': 'store_true',
        'default': None
    }


def AddEnableBinLog(parser, show_negated_in_help=False):
  kwargs = _GetKwargsForBoolFlag(show_negated_in_help)
  parser.add_argument(
      '--enable-bin-log',
      required=False,
      help=(
          'Specified if binary log should be enabled. If backup '
          'configuration is disabled, binary log must be disabled as well.'),
      **kwargs)


def AddFollowGAEApp(parser):
  parser.add_argument(
      '--follow-gae-app',
      required=False,
      help=('First Generation instances only. The App Engine app '
            'this instance should follow. It must be in the same region as '
            'the instance. WARNING: Instance may be restarted.'))


def AddMaintenanceReleaseChannel(parser):
  parser.add_argument(
      '--maintenance-release-channel',
      choices={
          'production': 'Production updates are stable and recommended '
                        'for applications in production.',
          'preview': 'Preview updates release prior to production '
                     'updates. You may wish to use the preview channel '
                     'for dev/test applications so that you can preview '
                     'their compatibility with your application prior '
                     'to the production release.'
      },
      type=lambda val: val.lower(),
      help="Which channel's updates to apply during the maintenance window. "
           "If not specified, Cloud SQL chooses the timing of updates to your "
           "instance.")


def AddMaintenanceWindowDay(parser):
  parser.add_argument(
      '--maintenance-window-day',
      choices=arg_parsers.DayOfWeek.DAYS,
      type=arg_parsers.DayOfWeek.Parse,
      help='Day of week for maintenance window, in UTC time zone.')


def AddMaintenanceWindowHour(parser):
  parser.add_argument(
      '--maintenance-window-hour',
      type=arg_parsers.BoundedInt(lower_bound=0, upper_bound=23),
      help='Hour of day for maintenance window, in UTC time zone.')


def AddMemory(parser):
  parser.add_argument(
      '--memory',
      type=arg_parsers.BinarySize(),
      required=False,
      help=('A whole number value indicating how much memory is desired in '
            'the machine. A size unit should be provided (eg. 3072MiB or '
            '9GiB) - if no units are specified, GiB is assumed. Both --cpu '
            'and --memory must be specified if a custom machine type is '
            'desired, and the --tier flag must be omitted.'))


def AddReplication(parser):
  parser.add_argument(
      '--replication',
      required=False,
      choices=['SYNCHRONOUS', 'ASYNCHRONOUS'],
      default=None,
      help='The type of replication this instance uses. The default is '
           'SYNCHRONOUS.')


def AddStorageAutoIncrease(parser):
  parser.add_argument(
      '--storage-auto-increase',
      action='store_true',
      default=None,
      help=('Storage size can be increased, but it cannot be decreased; '
            'storage increases are permanent for the life of the instance. '
            'With this setting enabled, a spike in storage requirements '
            'can result in permanently increased storage costs for your '
            'instance. However, if an instance runs out of available space, '
            'it can result in the instance going offline, dropping existing '
            'connections. This setting is enabled by default.'))


def AddStorageSize(parser):
  parser.add_argument(
      '--storage-size',
      type=arg_parsers.BinarySize(
          lower_bound='10GB',
          upper_bound='10230GB',
          suggested_binary_size_scales=['GB']),
      help=('Amount of storage allocated to the instance. Must be an integer '
            'number of GB between 10GB and 10230GB inclusive. The default is '
            '10GB.'))


# Database specific flags


def AddDatabaseName(parser):
  parser.add_argument(
      'database',
      completer=DatabaseCompleter,
      help='Cloud SQL database name.')


def AddCharset(parser):
  parser.add_argument(
      '--charset',
      help='Cloud SQL database charset setting, which specifies the '
      'set of symbols and encodings used to store the data in your database. '
      'Each database version may support a different set of charsets.')


def AddCollation(parser):
  parser.add_argument(
      '--collation',
      help='Cloud SQL database collation setting, which specifies '
      'the set of rules for comparing characters in a character set. Each'
      ' database version may support a different set of collations.')


def AddOperationArgument(parser):
  parser.add_argument(
      'operation',
      nargs='+',
      help='An identifier that uniquely identifies the operation.')


# Instance export / import flags.


def AddUriArgument(parser, help_text):
  """Add the 'uri' argument to the parser, with help text help_text."""
  parser.add_argument(
      'uri',
      help=help_text)


def AddDatabase(parser, help_text, required=False):
  """Add the '--database' flag to the parser, with help text help_text."""
  parser.add_argument(
      '--database',
      '-d',
      required=required,
      help=help_text)


def AddDatabaseList(parser, help_text):
  """Add the '--database' list flag to the parser, with help text help_text."""
  parser.add_argument(
      '--database',
      '-d',
      type=arg_parsers.ArgList(min_length=1),
      metavar='DATABASE',
      required=False,
      help=help_text)


def AddUser(parser, help_text):
  """Add the '--user' flag to the parser, with help text help_text."""
  parser.add_argument('--user', help=help_text)


INSTANCES_FORMAT = """
  table(
    instance:label=NAME,
    firstof(gceZone,region):label=LOCATION,
    settings.tier,
    ipAddresses[0].ipAddress.yesno(no="-"):label=ADDRESS,
    state:label=STATUS
  )
"""

INSTANCES_USERLABELS_FORMAT = """
  :(settings.userLabels:alias=labels:label=LABELS)
"""

INSTANCES_FORMAT_BETA = """
  {0}
  table(
    name,
    databaseVersion,
    firstof(gceZone,region):label=LOCATION,
    settings.tier,
    ipAddresses[0].ipAddress.yesno(no="-"):label=ADDRESS,
    state:label=STATUS
  )
""".format(INSTANCES_USERLABELS_FORMAT)

OPERATION_FORMAT = """
  table(
    operation,
    operationType:label=TYPE,
    startTime.iso():label=START,
    endTime.iso():label=END,
    error[0].code.yesno(no="-"):label=ERROR,
    state:label=STATUS
  )
"""

OPERATION_FORMAT_BETA = """
  table(
    name,
    operationType:label=TYPE,
    startTime.iso():label=START,
    endTime.iso():label=END,
    error[0].code.yesno(no="-"):label=ERROR,
    status:label=STATUS
  )
"""

CLIENT_CERTS_FORMAT = """
  table(
    commonName:label=NAME,
    sha1Fingerprint,
    expirationTime.yesno(no="-"):label=EXPIRATION
  )
"""

SERVER_CA_CERTS_FORMAT = """
  table(
    sha1Fingerprint,
    expirationTime.yesno(no="-"):label=EXPIRATION
  )
"""

TIERS_FORMAT = """
  table(
    tier,
    region.list():label=AVAILABLE_REGIONS,
    RAM.size(),
    DiskQuota.size():label=DISK
  )
"""

USERS_FORMAT_BETA = """
  table(
    name.yesno(no='(anonymous)'),
    host
  )
"""
