"""Generated message classes for fusiontables version v1.

API for working with Fusion Tables data.
"""
# NOTE: This file is autogenerated and should not be edited by hand.

from apitools.base.protorpclite import messages as _messages
from apitools.base.py import extra_types


package = 'fusiontables'


class Bucket(_messages.Message):
  """Specifies the minimum and maximum values, the color, opacity, icon and
  weight of a bucket within a StyleSetting.

  Fields:
    color: Color of line or the interior of a polygon in #RRGGBB format.
    icon: Icon name used for a point.
    max: Maximum value in the selected column for a row to be styled according
      to the bucket color, opacity, icon, or weight.
    min: Minimum value in the selected column for a row to be styled according
      to the bucket color, opacity, icon, or weight.
    opacity: Opacity of the color: 0.0 (transparent) to 1.0 (opaque).
    weight: Width of a line (in pixels).
  """

  color = _messages.StringField(1)
  icon = _messages.StringField(2)
  max = _messages.FloatField(3)
  min = _messages.FloatField(4)
  opacity = _messages.FloatField(5)
  weight = _messages.IntegerField(6, variant=_messages.Variant.INT32)


class Column(_messages.Message):
  """Specifies the id, name and type of a column in a table.

  Messages:
    BaseColumnValue: Optional identifier of the base column. If present, this
      column is derived from the specified base column.

  Fields:
    baseColumn: Optional identifier of the base column. If present, this
      column is derived from the specified base column.
    columnId: Identifier for the column.
    description: Optional column description.
    graph_predicate: Optional column predicate. Used to map table to graph
      data model (subject,predicate,object) See http://www.w3.org/TR/2014/REC-
      rdf11-concepts-20140225/#data-model
    kind: Type name: a template for an individual column.
    name: Required name of the column.
    type: Required type of the column.
  """

  class BaseColumnValue(_messages.Message):
    """Optional identifier of the base column. If present, this column is
    derived from the specified base column.

    Fields:
      columnId: The id of the column in the base table from which this column
        is derived.
      tableIndex: Offset to the entry in the list of base tables in the table
        definition.
    """

    columnId = _messages.IntegerField(1, variant=_messages.Variant.INT32)
    tableIndex = _messages.IntegerField(2, variant=_messages.Variant.INT32)

  baseColumn = _messages.MessageField('BaseColumnValue', 1)
  columnId = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  description = _messages.StringField(3)
  graph_predicate = _messages.StringField(4)
  kind = _messages.StringField(5, default=u'fusiontables#column')
  name = _messages.StringField(6)
  type = _messages.StringField(7)


class ColumnList(_messages.Message):
  """Represents a list of columns in a table.

  Fields:
    items: List of all requested columns.
    kind: Type name: a list of all columns.
    nextPageToken: Token used to access the next page of this result. No token
      is displayed if there are no more pages left.
    totalItems: Total number of columns for the table.
  """

  items = _messages.MessageField('Column', 1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#columnList')
  nextPageToken = _messages.StringField(3)
  totalItems = _messages.IntegerField(4, variant=_messages.Variant.INT32)


class FusiontablesColumnDeleteRequest(_messages.Message):
  """A FusiontablesColumnDeleteRequest object.

  Fields:
    columnId: Name or identifier for the column being deleted.
    tableId: Table from which the column is being deleted.
  """

  columnId = _messages.StringField(1, required=True)
  tableId = _messages.StringField(2, required=True)


class FusiontablesColumnDeleteResponse(_messages.Message):
  """An empty FusiontablesColumnDelete response."""


class FusiontablesColumnGetRequest(_messages.Message):
  """A FusiontablesColumnGetRequest object.

  Fields:
    columnId: Name or identifier for the column that is being requested.
    tableId: Table to which the column belongs.
  """

  columnId = _messages.StringField(1, required=True)
  tableId = _messages.StringField(2, required=True)


class FusiontablesColumnInsertRequest(_messages.Message):
  """A FusiontablesColumnInsertRequest object.

  Fields:
    column: A Column resource to be passed as the request body.
    tableId: Table for which a new column is being added.
  """

  column = _messages.MessageField('Column', 1)
  tableId = _messages.StringField(2, required=True)


class FusiontablesColumnListRequest(_messages.Message):
  """A FusiontablesColumnListRequest object.

  Fields:
    maxResults: Maximum number of columns to return. Optional. Default is 5.
    pageToken: Continuation token specifying which result page to return.
      Optional.
    tableId: Table whose columns are being listed.
  """

  maxResults = _messages.IntegerField(1, variant=_messages.Variant.UINT32)
  pageToken = _messages.StringField(2)
  tableId = _messages.StringField(3, required=True)


class FusiontablesColumnPatchRequest(_messages.Message):
  """A FusiontablesColumnPatchRequest object.

  Fields:
    column: A Column resource to be passed as the request body.
    columnId: Name or identifier for the column that is being updated.
    tableId: Table for which the column is being updated.
  """

  column = _messages.MessageField('Column', 1)
  columnId = _messages.StringField(2, required=True)
  tableId = _messages.StringField(3, required=True)


class FusiontablesColumnUpdateRequest(_messages.Message):
  """A FusiontablesColumnUpdateRequest object.

  Fields:
    column: A Column resource to be passed as the request body.
    columnId: Name or identifier for the column that is being updated.
    tableId: Table for which the column is being updated.
  """

  column = _messages.MessageField('Column', 1)
  columnId = _messages.StringField(2, required=True)
  tableId = _messages.StringField(3, required=True)


class FusiontablesQuerySqlGetRequest(_messages.Message):
  """A FusiontablesQuerySqlGetRequest object.

  Fields:
    hdrs: Should column names be included (in the first row)?. Default is
      true.
    sql: An SQL SELECT/SHOW/DESCRIBE statement.
    typed: Should typed values be returned in the (JSON) response -- numbers
      for numeric values and parsed geometries for KML values? Default is
      true.
  """

  hdrs = _messages.BooleanField(1)
  sql = _messages.StringField(2, required=True)
  typed = _messages.BooleanField(3)


class FusiontablesQuerySqlRequest(_messages.Message):
  """A FusiontablesQuerySqlRequest object.

  Fields:
    hdrs: Should column names be included (in the first row)?. Default is
      true.
    sql: An SQL SELECT/SHOW/DESCRIBE/INSERT/UPDATE/DELETE/CREATE statement.
    typed: Should typed values be returned in the (JSON) response -- numbers
      for numeric values and parsed geometries for KML values? Default is
      true.
  """

  hdrs = _messages.BooleanField(1)
  sql = _messages.StringField(2, required=True)
  typed = _messages.BooleanField(3)


class FusiontablesStyleDeleteRequest(_messages.Message):
  """A FusiontablesStyleDeleteRequest object.

  Fields:
    styleId: Identifier (within a table) for the style being deleted
    tableId: Table from which the style is being deleted
  """

  styleId = _messages.IntegerField(1, required=True, variant=_messages.Variant.INT32)
  tableId = _messages.StringField(2, required=True)


class FusiontablesStyleDeleteResponse(_messages.Message):
  """An empty FusiontablesStyleDelete response."""


class FusiontablesStyleGetRequest(_messages.Message):
  """A FusiontablesStyleGetRequest object.

  Fields:
    styleId: Identifier (integer) for a specific style in a table
    tableId: Table to which the requested style belongs
  """

  styleId = _messages.IntegerField(1, required=True, variant=_messages.Variant.INT32)
  tableId = _messages.StringField(2, required=True)


class FusiontablesStyleListRequest(_messages.Message):
  """A FusiontablesStyleListRequest object.

  Fields:
    maxResults: Maximum number of styles to return. Optional. Default is 5.
    pageToken: Continuation token specifying which result page to return.
      Optional.
    tableId: Table whose styles are being listed
  """

  maxResults = _messages.IntegerField(1, variant=_messages.Variant.UINT32)
  pageToken = _messages.StringField(2)
  tableId = _messages.StringField(3, required=True)


class FusiontablesTableCopyRequest(_messages.Message):
  """A FusiontablesTableCopyRequest object.

  Fields:
    copyPresentation: Whether to also copy tabs, styles, and templates.
      Default is false.
    tableId: ID of the table that is being copied.
  """

  copyPresentation = _messages.BooleanField(1)
  tableId = _messages.StringField(2, required=True)


class FusiontablesTableDeleteRequest(_messages.Message):
  """A FusiontablesTableDeleteRequest object.

  Fields:
    tableId: ID of the table that is being deleted.
  """

  tableId = _messages.StringField(1, required=True)


class FusiontablesTableDeleteResponse(_messages.Message):
  """An empty FusiontablesTableDelete response."""


class FusiontablesTableGetRequest(_messages.Message):
  """A FusiontablesTableGetRequest object.

  Fields:
    tableId: Identifier(ID) for the table being requested.
  """

  tableId = _messages.StringField(1, required=True)


class FusiontablesTableImportRowsRequest(_messages.Message):
  """A FusiontablesTableImportRowsRequest object.

  Fields:
    delimiter: The delimiter used to separate cell values. This can only
      consist of a single character. Default is ','.
    encoding: The encoding of the content. Default is UTF-8. Use 'auto-detect'
      if you are unsure of the encoding.
    endLine: The index of the last line from which to start importing,
      exclusive. Thus, the number of imported lines is endLine - startLine. If
      this parameter is not provided, the file will be imported until the last
      line of the file. If endLine is negative, then the imported content will
      exclude the last endLine lines. That is, if endline is negative, no line
      will be imported whose index is greater than N + endLine where N is the
      number of lines in the file, and the number of imported lines will be N
      + endLine - startLine.
    isStrict: Whether the CSV must have the same number of values for each
      row. If false, rows with fewer values will be padded with empty values.
      Default is true.
    startLine: The index of the first line from which to start importing,
      inclusive. Default is 0.
    tableId: The table into which new rows are being imported.
  """

  delimiter = _messages.StringField(1)
  encoding = _messages.StringField(2)
  endLine = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  isStrict = _messages.BooleanField(4)
  startLine = _messages.IntegerField(5, variant=_messages.Variant.INT32)
  tableId = _messages.StringField(6, required=True)


class FusiontablesTableImportTableRequest(_messages.Message):
  """A FusiontablesTableImportTableRequest object.

  Fields:
    delimiter: The delimiter used to separate cell values. This can only
      consist of a single character. Default is ','.
    encoding: The encoding of the content. Default is UTF-8. Use 'auto-detect'
      if you are unsure of the encoding.
    name: The name to be assigned to the new table.
  """

  delimiter = _messages.StringField(1)
  encoding = _messages.StringField(2)
  name = _messages.StringField(3, required=True)


class FusiontablesTableListRequest(_messages.Message):
  """A FusiontablesTableListRequest object.

  Fields:
    maxResults: Maximum number of styles to return. Optional. Default is 5.
    pageToken: Continuation token specifying which result page to return.
      Optional.
  """

  maxResults = _messages.IntegerField(1, variant=_messages.Variant.UINT32)
  pageToken = _messages.StringField(2)


class FusiontablesTablePatchRequest(_messages.Message):
  """A FusiontablesTablePatchRequest object.

  Fields:
    replaceViewDefinition: Should the view definition also be updated? The
      specified view definition replaces the existing one. Only a view can be
      updated with a new definition.
    table: A Table resource to be passed as the request body.
    tableId: ID of the table that is being updated.
  """

  replaceViewDefinition = _messages.BooleanField(1)
  table = _messages.MessageField('Table', 2)
  tableId = _messages.StringField(3, required=True)


class FusiontablesTableUpdateRequest(_messages.Message):
  """A FusiontablesTableUpdateRequest object.

  Fields:
    replaceViewDefinition: Should the view definition also be updated? The
      specified view definition replaces the existing one. Only a view can be
      updated with a new definition.
    table: A Table resource to be passed as the request body.
    tableId: ID of the table that is being updated.
  """

  replaceViewDefinition = _messages.BooleanField(1)
  table = _messages.MessageField('Table', 2)
  tableId = _messages.StringField(3, required=True)


class FusiontablesTaskDeleteRequest(_messages.Message):
  """A FusiontablesTaskDeleteRequest object.

  Fields:
    tableId: Table from which the task is being deleted.
    taskId: A string attribute.
  """

  tableId = _messages.StringField(1, required=True)
  taskId = _messages.StringField(2, required=True)


class FusiontablesTaskDeleteResponse(_messages.Message):
  """An empty FusiontablesTaskDelete response."""


class FusiontablesTaskGetRequest(_messages.Message):
  """A FusiontablesTaskGetRequest object.

  Fields:
    tableId: Table to which the task belongs.
    taskId: A string attribute.
  """

  tableId = _messages.StringField(1, required=True)
  taskId = _messages.StringField(2, required=True)


class FusiontablesTaskListRequest(_messages.Message):
  """A FusiontablesTaskListRequest object.

  Fields:
    maxResults: Maximum number of columns to return. Optional. Default is 5.
    pageToken: A string attribute.
    startIndex: A integer attribute.
    tableId: Table whose tasks are being listed.
  """

  maxResults = _messages.IntegerField(1, variant=_messages.Variant.UINT32)
  pageToken = _messages.StringField(2)
  startIndex = _messages.IntegerField(3, variant=_messages.Variant.UINT32)
  tableId = _messages.StringField(4, required=True)


class FusiontablesTemplateDeleteRequest(_messages.Message):
  """A FusiontablesTemplateDeleteRequest object.

  Fields:
    tableId: Table from which the template is being deleted
    templateId: Identifier for the template which is being deleted
  """

  tableId = _messages.StringField(1, required=True)
  templateId = _messages.IntegerField(2, required=True, variant=_messages.Variant.INT32)


class FusiontablesTemplateDeleteResponse(_messages.Message):
  """An empty FusiontablesTemplateDelete response."""


class FusiontablesTemplateGetRequest(_messages.Message):
  """A FusiontablesTemplateGetRequest object.

  Fields:
    tableId: Table to which the template belongs
    templateId: Identifier for the template that is being requested
  """

  tableId = _messages.StringField(1, required=True)
  templateId = _messages.IntegerField(2, required=True, variant=_messages.Variant.INT32)


class FusiontablesTemplateListRequest(_messages.Message):
  """A FusiontablesTemplateListRequest object.

  Fields:
    maxResults: Maximum number of templates to return. Optional. Default is 5.
    pageToken: Continuation token specifying which results page to return.
      Optional.
    tableId: Identifier for the table whose templates are being requested
  """

  maxResults = _messages.IntegerField(1, variant=_messages.Variant.UINT32)
  pageToken = _messages.StringField(2)
  tableId = _messages.StringField(3, required=True)


class Geometry(_messages.Message):
  """Represents a Geometry object.

  Fields:
    geometries: The list of geometries in this geometry collection.
    geometry: A extra_types.JsonValue attribute.
    type: Type: A collection of geometries.
  """

  geometries = _messages.MessageField('extra_types.JsonValue', 1, repeated=True)
  geometry = _messages.MessageField('extra_types.JsonValue', 2)
  type = _messages.StringField(3, default=u'GeometryCollection')


class Import(_messages.Message):
  """Represents an import request.

  Fields:
    kind: Type name: a template for an import request.
    numRowsReceived: The number of rows received from the import request.
  """

  kind = _messages.StringField(1, default=u'fusiontables#import')
  numRowsReceived = _messages.IntegerField(2)


class Line(_messages.Message):
  """Represents a line geometry.

  Messages:
    CoordinatesValueListEntry: Single entry in a CoordinatesValue.

  Fields:
    coordinates: The coordinates that define the line.
    type: Type: A line geometry.
  """

  class CoordinatesValueListEntry(_messages.Message):
    """Single entry in a CoordinatesValue.

    Fields:
      entry: A number attribute.
    """

    entry = _messages.FloatField(1, repeated=True)

  coordinates = _messages.MessageField('CoordinatesValueListEntry', 1, repeated=True)
  type = _messages.StringField(2, default=u'LineString')


class LineStyle(_messages.Message):
  """Represents a LineStyle within a StyleSetting

  Fields:
    strokeColor: Color of the line in #RRGGBB format.
    strokeColorStyler: Column-value, gradient or buckets styler that is used
      to determine the line color and opacity.
    strokeOpacity: Opacity of the line : 0.0 (transparent) to 1.0 (opaque).
    strokeWeight: Width of the line in pixels.
    strokeWeightStyler: Column-value or bucket styler that is used to
      determine the width of the line.
  """

  strokeColor = _messages.StringField(1)
  strokeColorStyler = _messages.MessageField('StyleFunction', 2)
  strokeOpacity = _messages.FloatField(3)
  strokeWeight = _messages.IntegerField(4, variant=_messages.Variant.INT32)
  strokeWeightStyler = _messages.MessageField('StyleFunction', 5)


class Point(_messages.Message):
  """Represents a point object.

  Fields:
    coordinates: The coordinates that define the point.
    type: Point: A point geometry.
  """

  coordinates = _messages.FloatField(1, repeated=True)
  type = _messages.StringField(2, default=u'Point')


class PointStyle(_messages.Message):
  """Represents a PointStyle within a StyleSetting

  Fields:
    iconName: Name of the icon. Use values defined in
      http://www.google.com/fusiontables/DataSource?dsrcid=308519
    iconStyler: Column or a bucket value from which the icon name is to be
      determined.
  """

  iconName = _messages.StringField(1)
  iconStyler = _messages.MessageField('StyleFunction', 2)


class Polygon(_messages.Message):
  """Represents a polygon object.

  Messages:
    CoordinatesValueListEntry: Single entry in a CoordinatesValue.

  Fields:
    coordinates: The coordinates that define the polygon.
    type: Type: A polygon geometry.
  """

  class CoordinatesValueListEntry(_messages.Message):
    """Single entry in a CoordinatesValue.

    Messages:
      EntryValueListEntry: Single entry in a EntryValue.

    Fields:
      entry: A EntryValueListEntry attribute.
    """

    class EntryValueListEntry(_messages.Message):
      """Single entry in a EntryValue.

      Fields:
        entry: A number attribute.
      """

      entry = _messages.FloatField(1, repeated=True)

    entry = _messages.MessageField('EntryValueListEntry', 1, repeated=True)

  coordinates = _messages.MessageField('CoordinatesValueListEntry', 1, repeated=True)
  type = _messages.StringField(2, default=u'Polygon')


class PolygonStyle(_messages.Message):
  """Represents a PolygonStyle within a StyleSetting

  Fields:
    fillColor: Color of the interior of the polygon in #RRGGBB format.
    fillColorStyler: Column-value, gradient, or bucket styler that is used to
      determine the interior color and opacity of the polygon.
    fillOpacity: Opacity of the interior of the polygon: 0.0 (transparent) to
      1.0 (opaque).
    strokeColor: Color of the polygon border in #RRGGBB format.
    strokeColorStyler: Column-value, gradient or buckets styler that is used
      to determine the border color and opacity.
    strokeOpacity: Opacity of the polygon border: 0.0 (transparent) to 1.0
      (opaque).
    strokeWeight: Width of the polyon border in pixels.
    strokeWeightStyler: Column-value or bucket styler that is used to
      determine the width of the polygon border.
  """

  fillColor = _messages.StringField(1)
  fillColorStyler = _messages.MessageField('StyleFunction', 2)
  fillOpacity = _messages.FloatField(3)
  strokeColor = _messages.StringField(4)
  strokeColorStyler = _messages.MessageField('StyleFunction', 5)
  strokeOpacity = _messages.FloatField(6)
  strokeWeight = _messages.IntegerField(7, variant=_messages.Variant.INT32)
  strokeWeightStyler = _messages.MessageField('StyleFunction', 8)


class Sqlresponse(_messages.Message):
  """Represents a response to an sql statement.

  Messages:
    RowsValueListEntry: Single entry in a RowsValue.

  Fields:
    columns: Columns in the table.
    kind: Type name: a template for an individual table.
    rows: The rows in the table. For each cell we print out whatever cell
      value (e.g., numeric, string) exists. Thus it is important that each
      cell contains only one value.
  """

  class RowsValueListEntry(_messages.Message):
    """Single entry in a RowsValue.

    Fields:
      entry: A extra_types.JsonValue attribute.
    """

    entry = _messages.MessageField('extra_types.JsonValue', 1, repeated=True)

  columns = _messages.StringField(1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#sqlresponse')
  rows = _messages.MessageField('RowsValueListEntry', 3, repeated=True)


class StandardQueryParameters(_messages.Message):
  """Query parameters accepted by all methods.

  Enums:
    AltValueValuesEnum: Data format for the response.

  Fields:
    alt: Data format for the response.
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters. Overrides userIp if both are provided.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    userIp: IP address of the site where the request originates. Use this if
      you want to enforce per-user limits.
  """

  class AltValueValuesEnum(_messages.Enum):
    """Data format for the response.

    Values:
      csv: Responses with Content-Type of text/csv
      json: Responses with Content-Type of application/json
    """
    csv = 0
    json = 1

  alt = _messages.EnumField('AltValueValuesEnum', 1, default=u'json')
  fields = _messages.StringField(2)
  key = _messages.StringField(3)
  oauth_token = _messages.StringField(4)
  prettyPrint = _messages.BooleanField(5, default=True)
  quotaUser = _messages.StringField(6)
  trace = _messages.StringField(7)
  userIp = _messages.StringField(8)


class StyleFunction(_messages.Message):
  """Represents a StyleFunction within a StyleSetting

  Messages:
    GradientValue: Gradient function that interpolates a range of colors based
      on column value.

  Fields:
    buckets: Bucket function that assigns a style based on the range a column
      value falls into.
    columnName: Name of the column whose value is used in the style.
    gradient: Gradient function that interpolates a range of colors based on
      column value.
    kind: Stylers can be one of three kinds: "fusiontables#fromColumn" if the
      column value is to be used as is, i.e., the column values can have
      colors in #RRGGBBAA format or integer line widths or icon names;
      "fusiontables#gradient" if the styling of the row is to be based on
      applying the gradient function on the column value; or
      "fusiontables#buckets" if the styling is to based on the bucket into
      which the the column value falls.
  """

  class GradientValue(_messages.Message):
    """Gradient function that interpolates a range of colors based on column
    value.

    Messages:
      ColorsValueListEntry: A ColorsValueListEntry object.

    Fields:
      colors: Array with two or more colors.
      max: Higher-end of the interpolation range: rows with this value will be
        assigned to colors[n-1].
      min: Lower-end of the interpolation range: rows with this value will be
        assigned to colors[0].
    """

    class ColorsValueListEntry(_messages.Message):
      """A ColorsValueListEntry object.

      Fields:
        color: Color in #RRGGBB format.
        opacity: Opacity of the color: 0.0 (transparent) to 1.0 (opaque).
      """

      color = _messages.StringField(1)
      opacity = _messages.FloatField(2)

    colors = _messages.MessageField('ColorsValueListEntry', 1, repeated=True)
    max = _messages.FloatField(2)
    min = _messages.FloatField(3)

  buckets = _messages.MessageField('Bucket', 1, repeated=True)
  columnName = _messages.StringField(2)
  gradient = _messages.MessageField('GradientValue', 3)
  kind = _messages.StringField(4)


class StyleSetting(_messages.Message):
  """Represents a complete StyleSettings object. The primary key is a
  combination of the tableId and a styleId.

  Fields:
    kind: Type name: an individual style setting. A StyleSetting contains the
      style defintions for points, lines, and polygons in a table. Since a
      table can have any one or all of them, a style definition can have
      point, line and polygon style definitions.
    markerOptions: Style definition for points in the table.
    name: Optional name for the style setting.
    polygonOptions: Style definition for polygons in the table.
    polylineOptions: Style definition for lines in the table.
    styleId: Identifier for the style setting (unique only within tables).
    tableId: Identifier for the table.
  """

  kind = _messages.StringField(1, default=u'fusiontables#styleSetting')
  markerOptions = _messages.MessageField('PointStyle', 2)
  name = _messages.StringField(3)
  polygonOptions = _messages.MessageField('PolygonStyle', 4)
  polylineOptions = _messages.MessageField('LineStyle', 5)
  styleId = _messages.IntegerField(6, variant=_messages.Variant.INT32)
  tableId = _messages.StringField(7)


class StyleSettingList(_messages.Message):
  """Represents a list of styles for a given table.

  Fields:
    items: All requested style settings.
    kind: Type name: in this case, a list of style settings.
    nextPageToken: Token used to access the next page of this result. No token
      is displayed if there are no more pages left.
    totalItems: Total number of styles for the table.
  """

  items = _messages.MessageField('StyleSetting', 1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#styleSettingList')
  nextPageToken = _messages.StringField(3)
  totalItems = _messages.IntegerField(4, variant=_messages.Variant.INT32)


class Table(_messages.Message):
  """Represents a table. Specifies the name, whether it is exportable,
  description, attribution, and attribution link.

  Fields:
    attribution: Optional attribution assigned to the table.
    attributionLink: Optional link for attribution.
    baseTableIds: Optional base table identifier if this table is a view or
      merged table.
    columns: Columns in the table.
    description: Optional description assigned to the table.
    isExportable: Variable for whether table is exportable.
    kind: Type name: a template for an individual table.
    name: Name assigned to a table.
    sql: Optional sql that encodes the table definition for derived tables.
    tableId: Encrypted unique alphanumeric identifier for the table.
  """

  attribution = _messages.StringField(1)
  attributionLink = _messages.StringField(2)
  baseTableIds = _messages.StringField(3, repeated=True)
  columns = _messages.MessageField('Column', 4, repeated=True)
  description = _messages.StringField(5)
  isExportable = _messages.BooleanField(6)
  kind = _messages.StringField(7, default=u'fusiontables#table')
  name = _messages.StringField(8)
  sql = _messages.StringField(9)
  tableId = _messages.StringField(10)


class TableList(_messages.Message):
  """Represents a list of tables.

  Fields:
    items: List of all requested tables.
    kind: Type name: a list of all tables.
    nextPageToken: Token used to access the next page of this result. No token
      is displayed if there are no more pages left.
  """

  items = _messages.MessageField('Table', 1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#tableList')
  nextPageToken = _messages.StringField(3)


class Task(_messages.Message):
  """Specifies the identifier, name, and type of a task in a table.

  Fields:
    kind: Type of the resource. This is always "fusiontables#task".
    progress: An indication of task progress.
    started: false while the table is busy with some other task. true if this
      background task is currently running.
    taskId: Identifier for the task.
    type: Type of background task. One of  DELETE_ROWS Deletes one or more
      rows from the table. ADD_ROWS "Adds one or more rows to a table.
      Includes importing data into a new table and importing more rows into an
      existing table. ADD_COLUMN Adds a new column to the table. CHANGE_TYPE
      Changes the type of a column.
  """

  kind = _messages.StringField(1, default=u'fusiontables#task')
  progress = _messages.StringField(2)
  started = _messages.BooleanField(3)
  taskId = _messages.IntegerField(4)
  type = _messages.StringField(5)


class TaskList(_messages.Message):
  """Represents a list of tasks for a table.

  Fields:
    items: List of all requested tasks.
    kind: Type of the resource. This is always "fusiontables#taskList".
    nextPageToken: Token used to access the next page of this result. No token
      is displayed if there are no more pages left.
    totalItems: Total number of tasks for the table.
  """

  items = _messages.MessageField('Task', 1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#taskList')
  nextPageToken = _messages.StringField(3)
  totalItems = _messages.IntegerField(4, variant=_messages.Variant.INT32)


class Template(_messages.Message):
  """Represents the contents of InfoWindow templates.

  Fields:
    automaticColumnNames: List of columns from which the template is to be
      automatically constructed. Only one of body or automaticColumns can be
      specified.
    body: Body of the template. It contains HTML with {column_name} to insert
      values from a particular column. The body is sanitized to remove certain
      tags, e.g., script. Only one of body or automaticColumns can be
      specified.
    kind: Type name: a template for the info window contents. The template can
      either include an HTML body or a list of columns from which the template
      is computed automatically.
    name: Optional name assigned to a template.
    tableId: Identifier for the table for which the template is defined.
    templateId: Identifier for the template, unique within the context of a
      particular table.
  """

  automaticColumnNames = _messages.StringField(1, repeated=True)
  body = _messages.StringField(2)
  kind = _messages.StringField(3, default=u'fusiontables#template')
  name = _messages.StringField(4)
  tableId = _messages.StringField(5)
  templateId = _messages.IntegerField(6, variant=_messages.Variant.INT32)


class TemplateList(_messages.Message):
  """Represents a list of templates for a given table.

  Fields:
    items: List of all requested templates.
    kind: Type name: a list of all templates.
    nextPageToken: Token used to access the next page of this result. No token
      is displayed if there are no more pages left.
    totalItems: Total number of templates for the table.
  """

  items = _messages.MessageField('Template', 1, repeated=True)
  kind = _messages.StringField(2, default=u'fusiontables#templateList')
  nextPageToken = _messages.StringField(3)
  totalItems = _messages.IntegerField(4, variant=_messages.Variant.INT32)

