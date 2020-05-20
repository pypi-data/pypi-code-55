from dataclasses import dataclass
from pyspark_config.yamlConfig.config import dataclass_json
from pyspark_config.spark_utils.dataframe_extended import DataFrame_Extended


@dataclass_json
@dataclass
class Source:
    type: str = None
    label: str = None
    path: str = None

    def apply(self, spark_session):
        pass


@dataclass_json
@dataclass
class Text(Source):
    type = "Text"

    def apply(self, spark_session):
        return spark_session.read.text(self.path)


@dataclass_json
@dataclass
class Csv(Source):
    r"""Loads a CSV file and returns the result as a  :class:`DataFrame`.

    This function will go through the input once to determine the input schema if
    ``inferSchema`` is enabled. To avoid going through the entire data once, disable
    ``inferSchema`` option or specify the schema explicitly using ``schema``.
    """
    type = "Csv"
    csv_path: str = None
    delimiter: str = ';'
    sep = None
    encoding = None
    quote = None
    escape = None
    comment = None
    header = None
    inferSchema = None
    ignoreLeadingWhiteSpace = None
    ignoreTrailingWhiteSpace = None
    nullValue = None
    nanValue = None
    positiveInf = None
    negativeInf = None
    dateFormat = None
    timestampFormat = None
    maxColumns = None
    maxCharsPerColumn = None
    maxMalformedLogPerPartition = None
    mode = None
    columnNameOfCorruptRecord = None
    multiLine = None
    charToEscapeQuoteEscaping = None
    samplingRatio = None
    enforceSchema = None
    emptyValue = None

    def apply(self, spark_session):
        return spark_session.read.option("delimiter", self.delimiter).csv(
            path=self.csv_path,
            sep=self.delimiter,
            encoding=self.encoding,
            quote=self.quote,
            escape=self.escape,
            comment=self.comment,
            header=self.header,
            inferSchema=self.inferSchema,
            ignoreLeadingWhiteSpace=self.ignoreLeadingWhiteSpace,
            ignoreTrailingWhiteSpace=self.ignoreTrailingWhiteSpace,
            nullValue=self.nullValue,
            nanValue=self.nanValue,
            positiveInf=self.positiveInf,
            negativeInf=self.negativeInf,
            dateFormat=self.dateFormat,
            timestampFormat=self.timestampFormat,
            maxColumns=self.maxColumns,
            maxCharsPerColumn=self.maxCharsPerColumn,
            maxMalformedLogPerPartition=self.maxMalformedLogPerPartition,
            mode=self.mode,
            columnNameOfCorruptRecord=self.columnNameOfCorruptRecord,
            multiLine=self.multiLine,
            charToEscapeQuoteEscaping=self.charToEscapeQuoteEscaping,
            samplingRatio=self.samplingRatio,
            enforceSchema=self.enforceSchema,
            emptyValue=self.emptyValue
        )


@dataclass
class Json(Source):
    """
    Loads JSON files and returns the results as a :class:`DataFrame`.

    `JSON Lines <http://jsonlines.org/>`_ (newline-delimited JSON) is supported by default.
    For JSON (one record per file), set the ``multiLine`` parameter to ``true``.

    If the ``schema`` parameter is not specified, this function goes
    through the input once to determine the input schema.

    """
    type = "Json"
    parquet_path: str = None
    primitivesAsString=None
    prefersDecimal=None
    allowComments=None
    allowUnquotedFieldNames=None
    allowSingleQuotes=None
    allowNumericLeadingZero=None
    allowBackslashEscapingAnyCharacter=None
    mode=None
    columnNameOfCorruptRecord=None
    dateFormat=None
    timestampFormat=None
    multiLine=None
    allowUnquotedControlChars=None
    lineSep=None
    samplingRatio=None
    dropFieldIfAllNull=None
    encoding=None

    def apply(self, spark_session):
        return spark_session.read.json(
            path=self.parquet_path,
            primitivesAsString=self.primitivesAsString,
            prefersDecimal=self.prefersDecimal,
            allowComments=self.allowComments,
            allowUnquotedFieldNames=self.allowUnquotedFieldNames,
            allowSingleQuotes=self.allowSingleQuotes,
            allowNumericLeadingZero=self.allowNumericLeadingZero,
            allowBackslashEscapingAnyCharacter=self.allowBackslashEscapingAnyCharacter,
            mode=self.mode,
            columnNameOfCorruptRecord=self.columnNameOfCorruptRecord,
            dateFormat=self.dateFormat,
            timestampFormat=self.timestampFormat,
            multiLine=self.multiLine,
            allowUnquotedControlChars=self.allowUnquotedControlChars,
            lineSep=self.lineSep,
            samplingRatio=self.samplingRatio,
            dropFieldIfAllNull=self.dropFieldIfAllNull,
            encoding=self.encoding
        )


@dataclass
class Parquet(Source):
    type = "Parquet"
    parquet_path: str = None

    def apply(self, spark_session):
        return spark_session.read.parquet(self.parquet_path)


@dataclass
class TFRecord(Source):
    type = "TFRecord"
    path: str = None

    def apply(self, spark_session):
        return spark_session.read.format("tfrecords").load(self.path)