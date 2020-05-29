    @staticmethod
    def groupBitAnd(x):
        return F('groupBitAnd', x)

    @staticmethod
    def groupBitOr(x):
        return F('groupBitOr', x)

    @staticmethod
    def groupBitXor(x):
        return F('groupBitXor', x)

    @staticmethod
    def CHARACTER_LENGTH(x):
        return F('CHARACTER_LENGTH', x)

    @staticmethod
    def CHAR_LENGTH(x):
        return F('CHAR_LENGTH', x)

    @staticmethod
    def covarPop(x, y):
        return F('covarPop', x, y)

    @staticmethod
    def covarSamp(x, y):
        return F('covarSamp', x, y)

    @staticmethod
    def IPv4CIDRToRange(x, y):
        return F('IPv4CIDRToRange', x, y)

    @staticmethod
    def IPv4NumToString(x):
        return F('IPv4NumToString', x)

    @staticmethod
    def IPv4NumToStringClassC(x):
        return F('IPv4NumToStringClassC', x)

    @staticmethod
    def IPv4StringToNum(x):
        return F('IPv4StringToNum', x)

    @staticmethod
    def IPv4ToIPv6(x):
        return F('IPv4ToIPv6', x)

    @staticmethod
    def IPv6CIDRToRange(x, y):
        return F('IPv6CIDRToRange', x, y)

    @staticmethod
    def IPv6NumToString(x):
        return F('IPv6NumToString', x)

    @staticmethod
    def IPv6StringToNum(x):
        return F('IPv6StringToNum', x)

    # JSONExtract: Function JSONExtract requires at least two arguments (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def JSONExtractBool(*args):
        return F('JSONExtractBool', *args)

    @staticmethod
    def JSONExtractFloat(*args):
        return F('JSONExtractFloat', *args)

    @staticmethod
    def JSONExtractInt(*args):
        return F('JSONExtractInt', *args)

    # JSONExtractKeysAndValues: Function JSONExtractKeysAndValues requires at least two arguments (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def JSONExtractRaw(*args):
        return F('JSONExtractRaw', *args)

    @staticmethod
    def JSONExtractString(*args):
        return F('JSONExtractString', *args)

    @staticmethod
    def JSONExtractUInt(*args):
        return F('JSONExtractUInt', *args)

    @staticmethod
    def JSONHas(*args):
        return F('JSONHas', *args)

    @staticmethod
    def JSONKey(*args):
        return F('JSONKey', *args)

    @staticmethod
    def JSONLength(*args):
        return F('JSONLength', *args)

    @staticmethod
    def JSONType(*args):
        return F('JSONType', *args)

    @staticmethod
    def MACNumToString(x):
        return F('MACNumToString', x)

    @staticmethod
    def MACStringToNum(x):
        return F('MACStringToNum', x)

    @staticmethod
    def MACStringToOUI(x):
        return F('MACStringToOUI', x)

    # OSHierarchy: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # OSIn: Embedded dictionaries were not loaded. You need to check configuration file.: Or unknown aggregate function OSIn. Maybe you meant: ['min'] (version 19.8.3.8 (official build)) (156)

    # OSToRoot: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # SEHierarchy: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # SEIn: Embedded dictionaries were not loaded. You need to check configuration file.: Or unknown aggregate function SEIn. Maybe you meant: ['min'] (version 19.8.3.8 (official build)) (156)

    # SEToRoot: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    @staticmethod
    def stddevPop(x):
        return F('stddevPop', x)

    @staticmethod
    def stddevSamp(x):
        return F('stddevSamp', x)

    @staticmethod
    def URLHierarchy(x):
        return F('URLHierarchy', x)

    @staticmethod
    def URLPathHierarchy(x):
        return F('URLPathHierarchy', x)

    @staticmethod
    def varPop(x):
        return F('varPop', x)

    @staticmethod
    def varSamp(x):
        return F('varSamp', x)

    @staticmethod
    def __bitSwapLastTwo(x):
        return F('__bitSwapLastTwo', x)


    # and: Number of arguments for function and doesn't match: passed 0, should be at least 2. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def any(x):
        return F('any', x)

    @staticmethod
    def anyHeavy(x):
        return F('anyHeavy', x)

    @staticmethod
    def anyLast(x):
        return F('anyLast', x)

    @staticmethod
    def argMax(x, y):
        return F('argMax', x, y)

    @staticmethod
    def argMin(x, y):
        return F('argMin', x, y)


    @staticmethod
    def assumeNotNull(x):
        return F('assumeNotNull', x)

    @staticmethod
    def avg(x):
        return F('avg', x)

    # bar: Function bar requires from 3 or 4 parameters: value, min_value, max_value, [max_width_of_bar = 80]. Passed 0. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def basename(x):
        return F('basename', x)

    @staticmethod
    def blockNumber():
        return F('blockNumber')

    @staticmethod
    def blockSize():
        return F('blockSize')

    @staticmethod
    def boundingRatio(x, y):
        return F('boundingRatio', x, y)

    # caseWithExpr: Function caseWithExpression expects at least 1 arguments (version 19.8.3.8 (official build)) (35)

    # caseWithExpression: Function caseWithExpression expects at least 1 arguments (version 19.8.3.8 (official build)) (35)

    # caseWithoutExpr: Invalid number of arguments for function multiIf (version 19.8.3.8 (official build)) (42)

    # caseWithoutExpression: Invalid number of arguments for function multiIf (version 19.8.3.8 (official build)) (42)


    # coalesce: No field class for Nothing

    # concatAssumeInjective: Number of arguments for function concatAssumeInjective doesn't match: passed 0, should be at least 2. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def corr(x, y):
        return F('corr', x, y)

    @staticmethod
    def corrStable(x, y):
        return F('corrStable', x, y)

    @staticmethod
    def count():
        return F('count')

    @staticmethod
    def covarPop(x, y):
        return F('covarPop', x, y)

    @staticmethod
    def covarPopStable(x, y):
        return F('covarPopStable', x, y)

    @staticmethod
    def covarSamp(x, y):
        return F('covarSamp', x, y)

    @staticmethod
    def covarSampStable(x, y):
        return F('covarSampStable', x, y)

    @staticmethod
    def currentDatabase():
        return F('currentDatabase')

    @staticmethod
    def cutFragment(x):
        return F('cutFragment', x)

    # cutIPv6: Number of arguments for function cutIPv6 doesn't match: passed 0, should be 3 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def cutQueryString(x):
        return F('cutQueryString', x)

    @staticmethod
    def cutQueryStringAndFragment(x):
        return F('cutQueryStringAndFragment', x)

    @staticmethod
    def cutToFirstSignificantSubdomain(x):
        return F('cutToFirstSignificantSubdomain', x)

    @staticmethod
    def cutURLParameter(x, y):
        return F('cutURLParameter', x, y)

    @staticmethod
    def cutWWW(x):
        return F('cutWWW', x)

    # dateDiff: Number of arguments for function dateDiff doesn't match: passed 0, should be 3 or 4 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def decodeURLComponent(x):
        return F('decodeURLComponent', x)

    @staticmethod
    def defaultValueOfArgumentType(x):
        return F('defaultValueOfArgumentType', x)

    @staticmethod
    def dictGet(dict_name, attr_name, id_expr):
        return F('dictGet', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetDate(dict_name, attr_name, id_expr):
        return F('dictGetDate', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetDateOrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetDateOrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetDateTime(dict_name, attr_name, id_expr):
        return F('dictGetDateTime', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetDateTimeOrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetDateTimeOrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetFloat32(dict_name, attr_name, id_expr):
        return F('dictGetFloat32', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetFloat32OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetFloat32OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetFloat64(dict_name, attr_name, id_expr):
        return F('dictGetFloat64', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetFloat64OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetFloat64OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetHierarchy(x, y):
        return F('dictGetHierarchy', x, y)

    @staticmethod
    def dictGetInt16(dict_name, attr_name, id_expr):
        return F('dictGetInt16', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetInt16OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetInt16OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetInt32(dict_name, attr_name, id_expr):
        return F('dictGetInt32', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetInt32OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetInt32OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetInt64(dict_name, attr_name, id_expr):
        return F('dictGetInt64', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetInt64OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetInt64OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetInt8(dict_name, attr_name, id_expr):
        return F('dictGetInt8', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetInt8OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetInt8OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetOrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetOrDefault', dict_name, attr_name, id_expr, default_value_expr)

    # dictGetString: Number of arguments for function dictGetString doesn't match: passed 0, should be 3 or 4. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def dictGetStringOrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetStringOrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetUInt16(dict_name, attr_name, id_expr):
        return F('dictGetUInt16', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetUInt16OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetUInt16OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetUInt32(dict_name, attr_name, id_expr):
        return F('dictGetUInt32', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetUInt32OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetUInt32OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetUInt64(dict_name, attr_name, id_expr):
        return F('dictGetUInt64', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetUInt64OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetUInt64OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetUInt8(dict_name, attr_name, id_expr):
        return F('dictGetUInt8', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetUInt8OrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetUInt8OrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictGetUUID(dict_name, attr_name, id_expr):
        return F('dictGetUUID', dict_name, attr_name, id_expr)

    @staticmethod
    def dictGetUUIDOrDefault(dict_name, attr_name, id_expr, default_value_expr):
        return F('dictGetUUIDOrDefault', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def dictHas(x, y):
        return F('dictHas', x, y)

    # dictIsIn: Number of arguments for function dictIsIn doesn't match: passed 0, should be 3 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def domain(x):
        return F('domain', x)

    @staticmethod
    def domainWithoutWWW(x):
        return F('domainWithoutWWW', x)

    @staticmethod
    def dumpColumnStructure(x):
        return F('dumpColumnStructure', x)

    @staticmethod
    def endsWith(x, y):
        return F('endsWith', x, y)

    # entropy: Incorrect number of arguments for aggregate function entropy (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def evalMLMethod(*args):
        return F('evalMLMethod', *args)

    @staticmethod
    def extract(x, y):
        return F('extract', x, y)

    @staticmethod
    def extractAll(x, y):
        return F('extractAll', x, y)

    @staticmethod
    def extractURLParameter(x, y):
        return F('extractURLParameter', x, y)

    @staticmethod
    def extractURLParameterNames(x):
        return F('extractURLParameterNames', x)

    @staticmethod
    def extractURLParameters(x):
        return F('extractURLParameters', x)

    @staticmethod
    def filesystemAvailable():
        return F('filesystemAvailable')

    @staticmethod
    def filesystemCapacity():
        return F('filesystemCapacity')

    @staticmethod
    def filesystemFree():
        return F('filesystemFree')

    @staticmethod
    def finalizeAggregation(x):
        return F('finalizeAggregation', x)

    @staticmethod
    def findClusterIndex(x, y):
        return F('findClusterIndex', x, y)

    @staticmethod
    def findClusterValue(x, y):
        return F('findClusterValue', x, y)

    @staticmethod
    def firstSignificantSubdomain(x):
        return F('firstSignificantSubdomain', x)

    @staticmethod
    def flatten(x):
        return F('flatten', x)

    # format: Number of arguments for function format doesn't match: passed 0, should be at least 1 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def formatReadableSize(x):
        return F('formatReadableSize', x)

    @staticmethod
    def fragment(x):
        return F('fragment', x)

    @staticmethod
    def geohashDecode(x):
        return F('geohashDecode', x)

    # geohashEncode: Incorrect number of arguments of function geohashEncode (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def getSizeOfEnumType(x):
        return F('getSizeOfEnumType', x)

    # globalIn: std::exception. Code: 1001, type: std::out_of_range, e.what() = vector::_M_range_check: __n (which is 1) >= this->size() (which is 0), version = 19.8.3.8 (official build)
 (0)

    # globalNotIn: std::exception. Code: 1001, type: std::out_of_range, e.what() = vector::_M_range_check: __n (which is 1) >= this->size() (which is 0), version = 19.8.3.8 (official build)
 (0)

    @staticmethod
    def greatCircleDistance(dict_name, attr_name, id_expr, default_value_expr):
        return F('greatCircleDistance', dict_name, attr_name, id_expr, default_value_expr)

    @staticmethod
    def greatest(x, y):
        return F('greatest', x, y)

    @staticmethod
    def groupArray(x):
        return F('groupArray', x)

    @staticmethod
    def groupArrayInsertAt(x, y):
        return F('groupArrayInsertAt', x, y)

    @staticmethod
    def groupBitAnd(x):
        return F('groupBitAnd', x)

    @staticmethod
    def groupBitOr(x):
        return F('groupBitOr', x)

    @staticmethod
    def groupBitXor(x):
        return F('groupBitXor', x)

    @staticmethod
    def groupBitmap(x):
        return F('groupBitmap', x)

    @staticmethod
    def groupUniqArray(x):
        return F('groupUniqArray', x)

    # hasColumnInTable: Invalid number of arguments for function hasColumnInTable (version 19.8.3.8 (official build)) (42)

    # histogram: Function histogram requires single parameter: bins count (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def hostName():
        return F('hostName')

    @staticmethod
    def identity(x):
        return F('identity', x)

    # if: Wrong number of arguments for function 'if' (0 instead of 3) (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def ifNull(x, y):
        return F('ifNull', x, y)

    @staticmethod
    def ignore():
        return F('ignore')

    @staticmethod
    def ignoreExceptNull():
        return F('ignoreExceptNull')

    # in: std::exception. Code: 1001, type: std::out_of_range, e.what() = vector::_M_range_check: __n (which is 1) >= this->size() (which is 0), version = 19.8.3.8 (official build)
 (0)

    @staticmethod
    def indexHint():
        return F('indexHint')

    @staticmethod
    def isFinite(x):
        return F('isFinite', x)

    @staticmethod
    def isInfinite(x):
        return F('isInfinite', x)

    @staticmethod
    def isNaN(x):
        return F('isNaN', x)

    @staticmethod
    def isNotNull(x):
        return F('isNotNull', x)

    @staticmethod
    def isNull(x):
        return F('isNull', x)

    @staticmethod
    def isValidUTF8(x):
        return F('isValidUTF8', x)

    # joinGet: Function joinGet takes 3 arguments (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def kurtPop(x):
        return F('kurtPop', x)

    @staticmethod
    def kurtSamp(x):
        return F('kurtSamp', x)

    @staticmethod
    def lcase(x):
        return F('lcase', x)

    @staticmethod
    def least(x, y):
        return F('least', x, y)

    @staticmethod
    def like(x, y):
        return F('like', x, y)

    # linearRegression: Aggregate function linearRegression requires at least two arguments: target and model's parameters (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def locate(x, y):
        return F('locate', x, y)
    position = locate

    # logisticRegression: Aggregate function logisticRegression requires at least two arguments: target and model's parameters (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def lowCardinalityIndices(x):
        return F('lowCardinalityIndices', x)

    @staticmethod
    def lowCardinalityKeys(x):
        return F('lowCardinalityKeys', x)

    @staticmethod
    def match(x, y):
        return F('match', x, y)

    @staticmethod
    def materialize(x):
        return F('materialize', x)

    @staticmethod
    def max(x):
        return F('max', x)

    @staticmethod
    def maxIntersections(x, y):
        return F('maxIntersections', x, y)

    @staticmethod
    def maxIntersectionsPosition(x, y):
        return F('maxIntersectionsPosition', x, y)

    @staticmethod
    def median(x):
        return F('median', x)
    quantile = median

    @staticmethod
    def medianDeterministic(x, y):
        return F('medianDeterministic', x, y)
    quantileDeterministic = medianDeterministic

    @staticmethod
    def medianExact(x):
        return F('medianExact', x)
    quantileExact = medianExact

    @staticmethod
    def medianExactWeighted(x, y):
        return F('medianExactWeighted', x, y)
    quantileExactWeighted = medianExactWeighted

    @staticmethod
    def medianTDigest(x):
        return F('medianTDigest', x)
    quantileTDigest = medianTDigest

    @staticmethod
    def medianTDigestWeighted(x, y):
        return F('medianTDigestWeighted', x, y)
    quantileTDigestWeighted = medianTDigestWeighted

    @staticmethod
    def medianTiming(x):
        return F('medianTiming', x)
    quantileTiming = medianTiming

    @staticmethod
    def medianTimingWeighted(x, y):
        return F('medianTimingWeighted', x, y)
    quantileTimingWeighted = medianTimingWeighted

    # mid: Number of arguments for function substring doesn't match: passed 0, should be 2 or 3 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def min(x):
        return F('min', x)

    # modelEvaluate: Function modelEvaluate expects at least 2 arguments (version 19.8.3.8 (official build)) (35)

    # multiFuzzyMatchAny: Number of arguments for function multiFuzzyMatchAny doesn't match: passed 0, should be 3 (version 19.8.3.8 (official build)) (42)

    # multiFuzzyMatchAnyIndex: Number of arguments for function multiFuzzyMatchAnyIndex doesn't match: passed 0, should be 3 (version 19.8.3.8 (official build)) (42)

    # multiIf: Invalid number of arguments for function multiIf (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def multiMatchAny(x, y):
        return F('multiMatchAny', x, y)

    @staticmethod
    def multiMatchAnyIndex(x, y):
        return F('multiMatchAnyIndex', x, y)

    @staticmethod
    def multiSearchAllPositions(x, y):
        return F('multiSearchAllPositions', x, y)

    @staticmethod
    def multiSearchAllPositionsCaseInsensitive(x, y):
        return F('multiSearchAllPositionsCaseInsensitive', x, y)

    @staticmethod
    def multiSearchAllPositionsCaseInsensitiveUTF8(x, y):
        return F('multiSearchAllPositionsCaseInsensitiveUTF8', x, y)

    @staticmethod
    def multiSearchAllPositionsUTF8(x, y):
        return F('multiSearchAllPositionsUTF8', x, y)

    @staticmethod
    def multiSearchAny(x, y):
        return F('multiSearchAny', x, y)

    @staticmethod
    def multiSearchAnyCaseInsensitive(x, y):
        return F('multiSearchAnyCaseInsensitive', x, y)

    @staticmethod
    def multiSearchAnyCaseInsensitiveUTF8(x, y):
        return F('multiSearchAnyCaseInsensitiveUTF8', x, y)

    @staticmethod
    def multiSearchAnyUTF8(x, y):
        return F('multiSearchAnyUTF8', x, y)

    @staticmethod
    def multiSearchFirstIndex(x, y):
        return F('multiSearchFirstIndex', x, y)

    @staticmethod
    def multiSearchFirstIndexCaseInsensitive(x, y):
        return F('multiSearchFirstIndexCaseInsensitive', x, y)

    @staticmethod
    def multiSearchFirstIndexCaseInsensitiveUTF8(x, y):
        return F('multiSearchFirstIndexCaseInsensitiveUTF8', x, y)

    @staticmethod
    def multiSearchFirstIndexUTF8(x, y):
        return F('multiSearchFirstIndexUTF8', x, y)

    @staticmethod
    def multiSearchFirstPosition(x, y):
        return F('multiSearchFirstPosition', x, y)

    @staticmethod
    def multiSearchFirstPositionCaseInsensitive(x, y):
        return F('multiSearchFirstPositionCaseInsensitive', x, y)

    @staticmethod
    def multiSearchFirstPositionCaseInsensitiveUTF8(x, y):
        return F('multiSearchFirstPositionCaseInsensitiveUTF8', x, y)

    @staticmethod
    def multiSearchFirstPositionUTF8(x, y):
        return F('multiSearchFirstPositionUTF8', x, y)

    @staticmethod
    def ngramDistance(x, y):
        return F('ngramDistance', x, y)

    @staticmethod
    def ngramDistanceCaseInsensitive(x, y):
        return F('ngramDistanceCaseInsensitive', x, y)

    @staticmethod
    def ngramDistanceCaseInsensitiveUTF8(x, y):
        return F('ngramDistanceCaseInsensitiveUTF8', x, y)

    @staticmethod
    def ngramDistanceUTF8(x, y):
        return F('ngramDistanceUTF8', x, y)

    @staticmethod
    def ngramSearch(x, y):
        return F('ngramSearch', x, y)

    @staticmethod
    def ngramSearchCaseInsensitive(x, y):
        return F('ngramSearchCaseInsensitive', x, y)

    @staticmethod
    def ngramSearchCaseInsensitiveUTF8(x, y):
        return F('ngramSearchCaseInsensitiveUTF8', x, y)

    @staticmethod
    def ngramSearchUTF8(x, y):
        return F('ngramSearchUTF8', x, y)

    # not: Syntax error: failed at position 14: FORMAT TabSeparatedWithNamesAndTypes. Expected non-empty parenthesized list of expressions (version 19.8.3.8 (official build)) (62)

    # notIn: std::exception. Code: 1001, type: std::out_of_range, e.what() = vector::_M_range_check: __n (which is 1) >= this->size() (which is 0), version = 19.8.3.8 (official build)
 (0)

    @staticmethod
    def notLike(x, y):
        return F('notLike', x, y)

    @staticmethod
    def nullIf(x, y):
        return F('nullIf', x, y)

    # or: Number of arguments for function or doesn't match: passed 0, should be at least 2. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def path(x):
        return F('path', x)

    @staticmethod
    def pathFull(x):
        return F('pathFull', x)

    # pointInEllipses: Incorrect number of arguments of function pointInEllipses. Must be 2 for your point plus 4 * N for ellipses (x_i, y_i, a_i, b_i). (version 19.8.3.8 (official build)) (42)

    # pointInPolygon: Too few arguments (version 19.8.3.8 (official build)) (35)

    @staticmethod
    def position(x, y):
        return F('position', x, y)

    @staticmethod
    def positionCaseInsensitive(x, y):
        return F('positionCaseInsensitive', x, y)

    @staticmethod
    def positionCaseInsensitiveUTF8(x, y):
        return F('positionCaseInsensitiveUTF8', x, y)

    @staticmethod
    def positionUTF8(x, y):
        return F('positionUTF8', x, y)

    @staticmethod
    def protocol(x):
        return F('protocol', x)

    @staticmethod
    def quantile(x):
        return F('quantile', x)

    @staticmethod
    def quantileDeterministic(x, y):
        return F('quantileDeterministic', x, y)

    @staticmethod
    def quantileExact(x):
        return F('quantileExact', x)

    @staticmethod
    def quantileExactWeighted(x, y):
        return F('quantileExactWeighted', x, y)

    @staticmethod
    def quantileTDigest(x):
        return F('quantileTDigest', x)

    @staticmethod
    def quantileTDigestWeighted(x, y):
        return F('quantileTDigestWeighted', x, y)

    @staticmethod
    def quantileTiming(x):
        return F('quantileTiming', x)

    @staticmethod
    def quantileTimingWeighted(x, y):
        return F('quantileTimingWeighted', x, y)

    @staticmethod
    def quantiles(x):
        return F('quantiles', x)

    @staticmethod
    def quantilesDeterministic(x, y):
        return F('quantilesDeterministic', x, y)

    @staticmethod
    def quantilesExact(x):
        return F('quantilesExact', x)

    @staticmethod
    def quantilesExactWeighted(x, y):
        return F('quantilesExactWeighted', x, y)

    @staticmethod
    def quantilesTDigest(x):
        return F('quantilesTDigest', x)

    @staticmethod
    def quantilesTDigestWeighted(x, y):
        return F('quantilesTDigestWeighted', x, y)

    @staticmethod
    def quantilesTiming(x):
        return F('quantilesTiming', x)

    @staticmethod
    def quantilesTimingWeighted(x, y):
        return F('quantilesTimingWeighted', x, y)

    @staticmethod
    def queryString(x):
        return F('queryString', x)

    @staticmethod
    def queryStringAndFragment(x):
        return F('queryStringAndFragment', x)

    # regionHierarchy: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionIn: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToArea: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToCity: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToContinent: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToCountry: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToDistrict: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToName: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToPopulation: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    # regionToTopContinent: Embedded dictionaries were not loaded. You need to check configuration file. (version 19.8.3.8 (official build)) (156)

    @staticmethod
    def reinterpretAsDate(x):
        return F('reinterpretAsDate', x)

    @staticmethod
    def reinterpretAsDateTime(x):
        return F('reinterpretAsDateTime', x)

    @staticmethod
    def reinterpretAsFixedString(x):
        return F('reinterpretAsFixedString', x)

    @staticmethod
    def reinterpretAsFloat32(x):
        return F('reinterpretAsFloat32', x)

    @staticmethod
    def reinterpretAsFloat64(x):
        return F('reinterpretAsFloat64', x)

    @staticmethod
    def reinterpretAsInt16(x):
        return F('reinterpretAsInt16', x)

    @staticmethod
    def reinterpretAsInt32(x):
        return F('reinterpretAsInt32', x)

    @staticmethod
    def reinterpretAsInt64(x):
        return F('reinterpretAsInt64', x)

    @staticmethod
    def reinterpretAsInt8(x):
        return F('reinterpretAsInt8', x)

    @staticmethod
    def reinterpretAsString(x):
        return F('reinterpretAsString', x)

    @staticmethod
    def reinterpretAsUInt16(x):
        return F('reinterpretAsUInt16', x)

    @staticmethod
    def reinterpretAsUInt32(x):
        return F('reinterpretAsUInt32', x)

    @staticmethod
    def reinterpretAsUInt64(x):
        return F('reinterpretAsUInt64', x)

    @staticmethod
    def reinterpretAsUInt8(x):
        return F('reinterpretAsUInt8', x)

    @staticmethod
    def replicate(x, y):
        return F('replicate', x, y)

    # retention: Not enough event arguments for aggregate function retention (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def rowNumberInAllBlocks():
        return F('rowNumberInAllBlocks')

    @staticmethod
    def rowNumberInBlock():
        return F('rowNumberInBlock')

    @staticmethod
    def runningAccumulate(x):
        return F('runningAccumulate', x)

    @staticmethod
    def runningDifference(x):
        return F('runningDifference', x)

    @staticmethod
    def runningDifferenceStartingWithFirstValue(x):
        return F('runningDifferenceStartingWithFirstValue', x)

    @staticmethod
    def sequenceCount(x):
        return F('sequenceCount', x)

    @staticmethod
    def sequenceMatch(x):
        return F('sequenceMatch', x)

    @staticmethod
    def simpleLinearRegression(x, y):
        return F('simpleLinearRegression', x, y)

    @staticmethod
    def skewPop(x):
        return F('skewPop', x)

    @staticmethod
    def skewSamp(x):
        return F('skewSamp', x)

    @staticmethod
    def sleep(x):
        return F('sleep', x)

    @staticmethod
    def sleepEachRow(x):
        return F('sleepEachRow', x)

    @staticmethod
    def startsWith(x, y):
        return F('startsWith', x, y)

    @staticmethod
    def stddevPop(x):
        return F('stddevPop', x)

    @staticmethod
    def stddevPopStable(x):
        return F('stddevPopStable', x)

    @staticmethod
    def stddevSamp(x):
        return F('stddevSamp', x)

    @staticmethod
    def stddevSampStable(x):
        return F('stddevSampStable', x)

    # substr: Number of arguments for function substring doesn't match: passed 0, should be 2 or 3 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def sum(x):
        return F('sum', x)

    @staticmethod
    def sumKahan(x):
        return F('sumKahan', x)

    # sumMap: Aggregate function sumMap requires at least two arguments of Array type. (version 19.8.3.8 (official build)) (42)

    # sumMapFiltered: Aggregate function sumMapFiltered requires exactly one parameter of Array type. (version 19.8.3.8 (official build)) (42)

    # sumMapFilteredWithOverflow: Aggregate function sumMapFilteredWithOverflow requires exactly one parameter of Array type. (version 19.8.3.8 (official build)) (42)

    # sumMapWithOverflow: Aggregate function sumMapWithOverflow requires at least two arguments of Array type. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def sumWithOverflow(x):
        return F('sumWithOverflow', x)

    @staticmethod
    def throwIf(x):
        return F('throwIf', x)

    # timeSeriesGroupRateSum: Not enough event arguments for aggregate function timeSeriesGroupRateSum (version 19.8.3.8 (official build)) (42)

    # timeSeriesGroupSum: Not enough event arguments for aggregate function timeSeriesGroupSum (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def timezone():
        return F('timezone')

    @staticmethod
    def toColumnTypeName(x):
        return F('toColumnTypeName', x)

    @staticmethod
    def toDateOrNull(d, timezone=None):
        return F('toDateOrNull', d, timezone) if timezone else F('toDateOrNull', d)

    @staticmethod
    def toDateOrZero(d, timezone=None):
        return F('toDateOrZero', d, timezone) if timezone else F('toDateOrZero', d)

    @staticmethod
    def toDateTimeOrNull(d, timezone=None):
        return F('toDateTimeOrNull', d, timezone) if timezone else F('toDateTimeOrNull', d)

    @staticmethod
    def toDateTimeOrZero(d, timezone=None):
        return F('toDateTimeOrZero', d, timezone) if timezone else F('toDateTimeOrZero', d)

    # toDayOfYear: Number of arguments for function toDayOfYear doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def toDecimal128OrNull(d, timezone=None):
        return F('toDecimal128OrNull', d, timezone) if timezone else F('toDecimal128OrNull', d)

    @staticmethod
    def toDecimal128OrZero(d, timezone=None):
        return F('toDecimal128OrZero', d, timezone) if timezone else F('toDecimal128OrZero', d)

    @staticmethod
    def toDecimal32OrNull(d, timezone=None):
        return F('toDecimal32OrNull', d, timezone) if timezone else F('toDecimal32OrNull', d)

    @staticmethod
    def toDecimal32OrZero(d, timezone=None):
        return F('toDecimal32OrZero', d, timezone) if timezone else F('toDecimal32OrZero', d)

    @staticmethod
    def toDecimal64OrNull(d, timezone=None):
        return F('toDecimal64OrNull', d, timezone) if timezone else F('toDecimal64OrNull', d)

    @staticmethod
    def toDecimal64OrZero(d, timezone=None):
        return F('toDecimal64OrZero', d, timezone) if timezone else F('toDecimal64OrZero', d)

    @staticmethod
    def toFloat32OrNull(d, timezone=None):
        return F('toFloat32OrNull', d, timezone) if timezone else F('toFloat32OrNull', d)

    @staticmethod
    def toFloat64OrNull(d, timezone=None):
        return F('toFloat64OrNull', d, timezone) if timezone else F('toFloat64OrNull', d)

    @staticmethod
    def toIPv4(x):
        return F('toIPv4', x)

    @staticmethod
    def toIPv6(x):
        return F('toIPv6', x)

    # toISOWeek: Number of arguments for function toISOWeek doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toISOYear: Number of arguments for function toISOYear doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def toInt16OrNull(d, timezone=None):
        return F('toInt16OrNull', d, timezone) if timezone else F('toInt16OrNull', d)

    @staticmethod
    def toInt32OrNull(d, timezone=None):
        return F('toInt32OrNull', d, timezone) if timezone else F('toInt32OrNull', d)

    @staticmethod
    def toInt64OrNull(d, timezone=None):
        return F('toInt64OrNull', d, timezone) if timezone else F('toInt64OrNull', d)

    @staticmethod
    def toInt8OrNull(d, timezone=None):
        return F('toInt8OrNull', d, timezone) if timezone else F('toInt8OrNull', d)

    # toIntervalDay: Number of arguments for function toIntervalDay doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalHour: Number of arguments for function toIntervalHour doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalMinute: Number of arguments for function toIntervalMinute doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalMonth: Number of arguments for function toIntervalMonth doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalQuarter: Number of arguments for function toIntervalQuarter doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalSecond: Number of arguments for function toIntervalSecond doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalWeek: Number of arguments for function toIntervalWeek doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    # toIntervalYear: Number of arguments for function toIntervalYear doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def toLowCardinality(x):
        return F('toLowCardinality', x)

    @staticmethod
    def toNullable(x):
        return F('toNullable', x)

    # toQuarter: Number of arguments for function toQuarter doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toRelativeQuarterNum: Number of arguments for function toRelativeQuarterNum doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toStartOfISOYear: Number of arguments for function toStartOfISOYear doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toStartOfInterval: Number of arguments for function toStartOfInterval doesn't match: passed 0, should be 2 or 3 (version 19.8.3.8 (official build)) (42)

    # toStartOfTenMinutes: Number of arguments for function toStartOfTenMinutes doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def toTimeZone(x, y):
        return F('toTimeZone', x, y)

    @staticmethod
    def toTypeName(x):
        return F('toTypeName', x)

    @staticmethod
    def toUInt16OrNull(d, timezone=None):
        return F('toUInt16OrNull', d, timezone) if timezone else F('toUInt16OrNull', d)

    @staticmethod
    def toUInt32OrNull(d, timezone=None):
        return F('toUInt32OrNull', d, timezone) if timezone else F('toUInt32OrNull', d)

    @staticmethod
    def toUInt64OrNull(d, timezone=None):
        return F('toUInt64OrNull', d, timezone) if timezone else F('toUInt64OrNull', d)

    @staticmethod
    def toUInt8OrNull(d, timezone=None):
        return F('toUInt8OrNull', d, timezone) if timezone else F('toUInt8OrNull', d)

    # toUnixTimestamp: Number of arguments for function toUnixTimestamp doesn't match: passed 0, should be 1 or 2. Second argument (time zone) is optional only make sense for DateTime. (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def toValidUTF8(x):
        return F('toValidUTF8', x)

    # toYYYYMM: Number of arguments for function toYYYYMM doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toYYYYMMDD: Number of arguments for function toYYYYMMDD doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    # toYYYYMMDDhhmmss: Number of arguments for function toYYYYMMDDhhmmss doesn't match: passed 0, should be 1 or 2 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def topK(x):
        return F('topK', x)

    @staticmethod
    def topKWeighted(x, y):
        return F('topKWeighted', x, y)

    @staticmethod
    def topLevelDomain(x):
        return F('topLevelDomain', x)

    # transform: Number of arguments for function transform doesn't match: passed 0, should be 3 or 4 (version 19.8.3.8 (official build)) (42)

    @staticmethod
    def trimBoth(x):
        return F('trimBoth', x)

    @staticmethod
    def trimLeft(x):
        return F('trimLeft', x)

    @staticmethod
    def trimRight(x):
        return F('trimRight', x)

    @staticmethod
    def trunc(x, y=None):
        return F('trunc', x, y) if y else F('trunc', x)

    @staticmethod
    def truncate(x, y=None):
        return F('truncate', x, y) if y else F('truncate', x)
    trunc = truncate

    @staticmethod
    def tuple(*args):
        return F('tuple', *args)

    @staticmethod
    def tupleElement(x, y):
        return F('tupleElement', x, y)

    @staticmethod
    def ucase(x):
        return F('ucase', x)

    @staticmethod
    def uniq(*args):
        return F('uniq', *args)

    @staticmethod
    def uniqCombined(*args):
        return F('uniqCombined', *args)

    @staticmethod
    def uniqExact(*args):
        return F('uniqExact', *args)

    @staticmethod
    def uniqHLL12(*args):
        return F('uniqHLL12', *args)

    @staticmethod
    def uniqUpTo(*args):
        return F('uniqUpTo', *args)

    @staticmethod
    def uptime():
        return F('uptime')

    @staticmethod
    def varPop(x):
        return F('varPop', x)

    @staticmethod
    def varPopStable(x):
        return F('varPopStable', x)

    @staticmethod
    def varSamp(x):
        return F('varSamp', x)

    @staticmethod
    def varSampStable(x):
        return F('varSampStable', x)

    @staticmethod
    def version():
        return F('version')

    @staticmethod
    def visibleWidth(x):
        return F('visibleWidth', x)

    @staticmethod
    def visitParamExtractBool(x, y):
        return F('visitParamExtractBool', x, y)

    @staticmethod
    def visitParamExtractFloat(x, y):
        return F('visitParamExtractFloat', x, y)

    @staticmethod
    def visitParamExtractInt(x, y):
        return F('visitParamExtractInt', x, y)

    @staticmethod
    def visitParamExtractRaw(x, y):
        return F('visitParamExtractRaw', x, y)

    @staticmethod
    def visitParamExtractString(x, y):
        return F('visitParamExtractString', x, y)

    @staticmethod
    def visitParamExtractUInt(x, y):
        return F('visitParamExtractUInt', x, y)

    @staticmethod
    def visitParamHas(x, y):
        return F('visitParamHas', x, y)

    @staticmethod
    def windowFunnel(x):
        return F('windowFunnel', x)

    # xor: Number of arguments for function xor doesn't match: passed 0, should be at least 2. (version 19.8.3.8 (official build)) (42)

