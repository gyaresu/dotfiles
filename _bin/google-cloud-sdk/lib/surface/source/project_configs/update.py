# Copyright 2018 Google Inc. All Rights Reserved.
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
"""`gcloud source project-configs update` command."""

from __future__ import absolute_import
from __future__ import unicode_literals

from googlecloudsdk.api_lib.source import project_configs
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.source import flags
from googlecloudsdk.command_lib.source import util


class Update(base.Command):
  """Update the Cloud Source Repositories configuration of the current project.
  """

  @staticmethod
  def Args(parser):
    flags.AddPushblockFlagsToParser(parser)

  def Run(self, args):
    client = project_configs.ProjectConfig()
    updated_project_config = util.ParseProjectConfig(args)
    return client.Update(updated_project_config, 'enablePrivateKeyCheck')
