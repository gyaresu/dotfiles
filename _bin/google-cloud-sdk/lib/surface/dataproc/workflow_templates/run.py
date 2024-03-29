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
"""Run a workflow template."""
from __future__ import absolute_import
from __future__ import unicode_literals
import uuid

from googlecloudsdk.api_lib.dataproc import dataproc as dp
from googlecloudsdk.api_lib.dataproc import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.dataproc import flags
from googlecloudsdk.core import log


@base.Deprecate(is_removed=False,
                warning='Workflow template run command is deprecated, please '
                        'use instantiate command: "gcloud beta dataproc '
                        'workflow-templates instantiate"')
@base.ReleaseTracks(base.ReleaseTrack.BETA)
class Run(base.CreateCommand):
  """Run a workflow template."""

  @staticmethod
  def Args(parser):
    flags.AddTemplateFlag(parser, 'run')
    flags.AddTimeoutFlag(parser, default='24h')
    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    # TODO (b/68774667): deprecate Run command in favor of Instantiate command.
    dataproc = dp.Dataproc(self.ReleaseTrack())
    msgs = dataproc.messages
    template = util.ParseWorkflowTemplates(args.template, dataproc)

    instantiate_request = dataproc.messages.InstantiateWorkflowTemplateRequest()
    instantiate_request.instanceId = uuid.uuid4().hex  # request UUID

    request = msgs.DataprocProjectsRegionsWorkflowTemplatesInstantiateRequest(
        instantiateWorkflowTemplateRequest=instantiate_request,
        name=template.RelativeName())

    operation = dataproc.client.projects_regions_workflowTemplates.Instantiate(
        request)
    if args.async:
      log.status.Print('Running [{0}].'.format(template.Name()))
      return

    operation = util.WaitForWorkflowTemplateOperation(
        dataproc, operation, timeout_s=args.timeout)
    return operation
