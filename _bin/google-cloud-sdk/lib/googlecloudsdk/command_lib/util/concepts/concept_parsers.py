# Copyright 2017 Google Inc. All Rights Reserved.
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
"""Classes to define how concept args are added to argparse.

A PresentationSpec is used to define how a concept spec is presented in an
individual command, such as its help text. ResourcePresentationSpecs are
used for resource specs.

ConceptParsers are parsers used to manage the adding of all concept arguments
to a given command's argparse parser. The ConceptParser is created with a list
of all resources needed for the command, and they should be added all at once
during calliope's Args method.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from googlecloudsdk.calliope.concepts import deps
from googlecloudsdk.calliope.concepts import handlers
from googlecloudsdk.calliope.concepts import util
from googlecloudsdk.command_lib.util.concepts import info_holders

import six


class PresentationSpec(object):
  """Class that defines how concept arguments are presented in a command."""

  @property
  def concept_spec(self):
    """The ConceptSpec associated with the PresentationSpec.

    Must be overridden in subclasses.

    Returns:
      (googlecloudsdk.calliope.concepts.ConceptSpec) the concept spec.
    """
    raise NotImplementedError

  @property
  def attribute_to_args_map(self):
    """The map of attribute names to associated args.

    Must be overridden in subclasses.

    Returns:
      {str: str}, the map.
    """
    raise NotImplementedError

  def _GenerateInfo(self, fallthroughs_map):
    """Generate a ConceptInfo object for the ConceptParser.

    Must be overridden in subclasses.

    Args:
      fallthroughs_map: {str: [googlecloudsdk.calliope.concepts.deps.
        _FallthroughBase]}, dict keyed by attribute name to lists of
        fallthroughs.

    Returns:
      info_holders.ConceptInfo, the ConceptInfo object.
    """
    raise NotImplementedError


class ResourcePresentationSpec(PresentationSpec):
  """Class that specifies how concept arguments are presented in a command.

  Attributes:
    name: str, the name of the main arg for the concept. Can be positional or
      flag style (UPPER_SNAKE_CASE or --lower-train-case).
    concept_spec: googlecloudsdk.calliope.concepts.ConceptSpec, The spec that
      specifies the concept.
    group_help: str, the help text for the entire arg group.
    prefixes: bool, whether to use prefixes before the attribute flags, such as
      `--myresource-project`.
    required: bool, whether the anchor argument should be required. If True, the
      command will fail at argparse time if the anchor argument isn't given.
    plural: bool, True if the resource will be parsed as a list, False
      otherwise.
    group: the parser or subparser for a Calliope command that the resource
      arguments should be added to. If not provided, will be added to the main
      parser.
  """

  def __init__(self, name, concept_spec, group_help, prefixes=False,
               required=False, flag_name_overrides=None, plural=False,
               group=None):
    """Initializes a ResourcePresentationSpec.

    Args:
      name: str, the name of the main arg for the concept.
      concept_spec: googlecloudsdk.calliope.concepts.ConceptSpec, The spec that
        specifies the concept.
      group_help: str, the help text for the entire arg group.
      prefixes: bool, whether to use prefixes before the attribute flags, such
        as `--myresource-project`.
      required: bool, whether the anchor argument should be required.
      flag_name_overrides: {str: str}, dict of attribute names to the desired
        flag name. To remove a flag altogether, use '' as its rename value.
      plural: bool, True if the resource will be parsed as a list, False
        otherwise.
      group: the parser or subparser for a Calliope command that the resource
        arguments should be added to. If not provided, will be added to the main
        parser.
    """
    self.name = name
    self._concept_spec = concept_spec
    self.group_help = group_help
    self.prefixes = prefixes
    self.required = required
    self.plural = plural
    self.group = group

    # Create a rename map for the attributes to their flags.
    self._attribute_to_args_map = {}
    for i, attribute in enumerate(self._concept_spec.attributes):
      is_anchor = i == len(self._concept_spec.attributes) - 1
      name = self.GetFlagName(
          attribute.name, self.name, flag_name_overrides, prefixes,
          is_anchor=is_anchor)
      if name:
        self._attribute_to_args_map[attribute.name] = name

  @property
  def attribute_to_args_map(self):
    return self._attribute_to_args_map

  @staticmethod
  def GetFlagName(attribute_name, presentation_name, flag_name_overrides=None,
                  prefixes=False, is_anchor=False):
    """Gets the flag name for a given attribute name.

    Returns a flag name for an attribute, adding prefixes as necessary or using
    overrides if an override map is provided.

    Args:
      attribute_name: str, the name of the attribute to base the flag name on.
      presentation_name: str, the anchor argument name of the resource the
        attribute belongs to (e.g. '--foo').
      flag_name_overrides: {str: str}, a dict of attribute names to exact string
        of the flag name to use for the attribute. None if no overrides.
      prefixes: bool, whether to use the resource name as a prefix for the flag.
      is_anchor: bool, True if this it he anchor flag, False otherwise.

    Returns:
      (str) the name of the flag.
    """
    flag_name_overrides = flag_name_overrides or {}
    if attribute_name in flag_name_overrides:
      return flag_name_overrides.get(attribute_name)
    if attribute_name == 'project':
      return ''
    if is_anchor:
      return presentation_name
    prefix = util.PREFIX
    if prefixes:
      if presentation_name.startswith(util.PREFIX):
        prefix += presentation_name[len(util.PREFIX):] + '-'
      else:
        prefix += presentation_name.lower().replace('_', '-') + '-'
    return prefix + attribute_name

  @property
  def concept_spec(self):
    return self._concept_spec

  def _GenerateInfo(self, fallthroughs_map):
    """Gets the ResourceInfo object for the ConceptParser.

    Args:
      fallthroughs_map: {str: [googlecloudsdk.calliope.concepts.deps.
        _FallthroughBase]}, dict keyed by attribute name to lists of
        fallthroughs.

    Returns:
      info_holders.ResourceInfo, the ResourceInfo object.
    """
    return info_holders.ResourceInfo(
        self.name,
        self.concept_spec,
        self.group_help,
        self.attribute_to_args_map,
        fallthroughs_map,
        required=self.required,
        plural=self.plural,
        group=self.group)

  def __eq__(self, other):
    if not isinstance(other, type(self)):
      return False
    return (self.name == other.name and
            self.concept_spec == other.concept_spec and
            self.group_help == other.group_help and
            self.prefixes == other.prefixes and
            self.plural == other.plural and
            self.required == other.required and
            self.group == other.group)


class ConceptParser(object):
  """Class that handles adding concept specs to argparse."""

  def __init__(self, presentation_specs, command_level_fallthroughs=None):
    """Initializes a concept holder.

    Args:
      presentation_specs: [PresentationSpec], a list of the specs for concepts
        to be added to the parser.
      command_level_fallthroughs: {str: str}, a map of attributes to argument
        fallthroughs for those attributes. The format of the key should be FOO.a
        (the resource presentation name is "FOO" and the attribute name is "a").
        The format of the value should either be "BAR.b" (where the argument
        depended upon is the main argument generated for attribute "b" of
        the resource presentation spec that is named "BAR"), or "--baz", where
        "--baz" is a non-resource argument that is added separately to the
        parser.

    Raises:
      ValueError: if two presentation specs have the same name or two specs
        contain positional arguments.
    """
    self._specs = {}
    self._all_args = []
    self._runtime_handler = handlers.RuntimeHandler()
    for spec in presentation_specs:
      self._AddSpec(spec)
    self._command_level_fallthroughs = self._ValidateAndFormatFallthroughsMap(
        command_level_fallthroughs or {})

  @classmethod
  def ForResource(cls, name, resource_spec, group_help, required=False,
                  flag_name_overrides=None, plural=False, prefixes=False,
                  group=None, command_level_fallthroughs=None):
    """Constructs a ConceptParser for a single resource argument.

    Automatically sets prefixes to False.

    Args:
      name: str, the name of the main arg for the resource.
      resource_spec: googlecloudsdk.calliope.concepts.ResourceSpec, The spec
        that specifies the resource.
      group_help: str, the help text for the entire arg group.
      required: bool, whether the main argument should be required for the
        command.
      flag_name_overrides: {str: str}, dict of attribute names to the desired
        flag name. To remove a flag altogether, use '' as its rename value.
      plural: bool, True if the resource will be parsed as a list, False
        otherwise.
      prefixes: bool, True if flag names will be prefixed with the resource
        name, False otherwise. Should be False for all typical use cases.
      group: the parser or subparser for a Calliope command that the resource
        arguments should be added to. If not provided, will be added to the main
        parser.
      command_level_fallthroughs: a map of attribute names to lists of command-
        specific fallthroughs. These will be prioritized over the default
        fallthroughs for the attribute.

    Returns:
      (googlecloudsdk.calliope.concepts.concept_parsers.ConceptParser) The fully
        initialized ConceptParser.
    """
    presentation_spec = ResourcePresentationSpec(
        name,
        resource_spec,
        group_help,
        required=required,
        flag_name_overrides=flag_name_overrides or {},
        plural=plural,
        prefixes=prefixes,
        group=group)
    fallthroughs_map = {}
    for attribute_name, fallthroughs in six.iteritems(
        command_level_fallthroughs or {}):
      key = '{}.{}'.format(presentation_spec.name, attribute_name)
      fallthroughs_map[key] = fallthroughs
    return cls([presentation_spec], fallthroughs_map)

  def _ArgNameMatches(self, name, other_name):
    """Checks if two argument names match in the namespace.

    RESOURCE_ARG and --resource-arg will match with each other, as well as exact
    matches.

    Args:
      name: the first argument name.
      other_name: the second argument name.

    Returns:
      (bool) True if the names match.
    """
    if util.NormalizeFormat(name) == util.NormalizeFormat(other_name):
      return True
    return False

  def _AddSpec(self, presentation_spec):
    """Adds a given presentation spec to the concept holder's spec registry.

    Args:
      presentation_spec: PresentationSpec, the spec to be added.

    Raises:
      ValueError: if two presentation specs have the same name, if two
        presentation specs are both positional, or if two args are going to
        overlap.
    """
    # Check for duplicate spec names.
    for spec_name in self._specs:
      if self._ArgNameMatches(spec_name, presentation_spec.name):
        raise ValueError('Attempted to add two concepts with the same name: '
                         '[{}, {}]'.format(spec_name, presentation_spec.name))
      if (util.IsPositional(spec_name) and
          util.IsPositional(presentation_spec.name)):
        raise ValueError('Attempted to add multiple concepts with positional '
                         'arguments: [{}, {}]'.format(spec_name,
                                                      presentation_spec.name))

    # Also check for duplicate argument names.
    for a, arg_name in six.iteritems(presentation_spec.attribute_to_args_map):
      del a  # Unused.
      name = util.NormalizeFormat(arg_name)
      if name in self._all_args:
        raise ValueError('Attempted to add a duplicate argument name: [{}]'
                         .format(arg_name))
      self._all_args.append(name)

    self._specs[presentation_spec.name] = presentation_spec

  def _ValidateAndFormatFallthroughsMap(self, command_level_fallthroughs):
    """Validate formatting of fallthroughs and build map keyed to spec name."""
    spec_map = {}
    for key, fallthroughs_list in six.iteritems(command_level_fallthroughs):
      keys = key.split('.')
      if len(keys) != 2:
        raise ValueError('invalid fallthrough key: [{}]. Must be in format '
                         '"FOO.a" where FOO is the presentation spec name and '
                         'a is the attribute name.'.format(key))
      spec_name, attribute_name = keys
      self._ValidateSpecAndAttributeExist('key', spec_name, attribute_name)
      for fallthrough_string in fallthroughs_list:
        values = fallthrough_string.split('.')
        if len(values) not in [1, 2]:
          raise ValueError('invalid fallthrough value: [{}]. Must be in the '
                           'form BAR.b or --baz'.format(fallthrough_string))
        if len(values) == 2:
          value_spec_name, value_attribute_name = values
          self._ValidateSpecAndAttributeExist('value',
                                              value_spec_name,
                                              value_attribute_name)
      spec_map.setdefault(spec_name, {})[attribute_name] = fallthroughs_list
    return spec_map

  def _ValidateSpecAndAttributeExist(self, location, spec_name, attribute_name):
    """Raises if a formatted string refers to non-existent spec or attribute."""
    if spec_name not in self.specs:
      raise ValueError('invalid fallthrough {}: [{}]. Spec name is not '
                       'present in the presentation specs. Available names: '
                       '[{}]'.format(
                           location,
                           '{}.{}'.format(spec_name, attribute_name),
                           ', '.join(sorted(list(self.specs.keys())))))
    spec = self.specs.get(spec_name)
    if attribute_name not in [
        attribute.name for attribute in spec.concept_spec.attributes]:
      raise ValueError('invalid fallthrough {}: [{}]. spec named [{}] has no '
                       'attribute named [{}]'.format(
                           location,
                           '{}.{}'.format(spec_name, attribute_name),
                           spec_name,
                           attribute_name))

  @property
  def specs(self):
    return self._specs

  def AddToParser(self, parser):
    """Adds attribute args for all presentation specs to argparse.

    Args:
      parser: the parser for a Calliope command.
    """
    parser.add_concepts(self._runtime_handler)
    for spec_name, spec in six.iteritems(self._specs):
      concept_info = self.GetInfo(spec_name)
      concept_info.AddToParser(parser)
      self._runtime_handler.AddConcept(
          util.NormalizeFormat(spec_name),
          concept_info,
          required=spec.required)

  def GetExampleArgString(self):
    """Returns a command line example arg string for the concept."""
    examples = []
    for spec_name in self._specs:
      info = self.GetInfo(spec_name)
      args = info.GetExampleArgList()
      if args:
        examples.extend(args)

    def _PositionalsFirst(arg):
      prefix = 'Z' if arg.startswith('--') else 'A'
      return prefix + arg

    return ' '.join(sorted(examples, key=_PositionalsFirst))

  def _MakeFallthrough(self, fallthrough_string):
    """Make an ArgFallthrough from a formatted string."""
    values = fallthrough_string.split('.')
    if len(values) == 1:
      arg_name = values
      return deps.ArgFallthrough(values[0])
    elif len(values) == 2:
      spec_name, attribute_name = values
      spec = self.specs.get(spec_name)
      arg_name = spec.attribute_to_args_map.get(attribute_name, None)
      if not arg_name:
        raise ValueError(
            'Invalid fallthrough value [{}]: No argument associated with '
            'attribute [{}] in concept argument named [{}]'.format(
                fallthrough_string,
                attribute_name,
                spec_name))
      return deps.ArgFallthrough(arg_name)
    else:
      # Defensive only, should be validated earlier
      raise ValueError('bad fallthrough string [{}]'.format(fallthrough_string))

  def GetInfo(self, presentation_spec_name):
    """Build ConceptInfo object for the spec with the given name."""
    if presentation_spec_name not in self.specs:
      raise ValueError('Presentation spec with name [{}] has not been added '
                       'to the concept parser, cannot generate info.'.format(
                           presentation_spec_name))
    presentation_spec = self.specs[presentation_spec_name]
    fallthroughs_map = {}
    for attribute in presentation_spec.concept_spec.attributes:
      fallthrough_strings = self._command_level_fallthroughs.get(
          presentation_spec.name, {}).get(attribute.name, [])
      fallthroughs = [self._MakeFallthrough(fallthrough_string)
                      for fallthrough_string in fallthrough_strings]
      fallthroughs_map[attribute.name] = fallthroughs + attribute.fallthroughs

    return presentation_spec._GenerateInfo(fallthroughs_map)  # pylint: disable=protected-access
