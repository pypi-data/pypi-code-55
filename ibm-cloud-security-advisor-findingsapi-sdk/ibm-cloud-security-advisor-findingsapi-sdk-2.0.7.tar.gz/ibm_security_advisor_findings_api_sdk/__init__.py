# coding: utf-8
# Copyright 2019 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ibm_cloud_sdk_core import IAMTokenManager, DetailedResponse, BaseService, ApiException

from .common import get_sdk_headers
from .version import __version__
from .findings_api_v1 import FindingsApiV1
from .findings_api_v1 import Card
from .findings_api_v1 import CardElement
from .findings_api_v1 import Certainty
from .findings_api_v1 import Context
from .findings_api_v1 import DataTransferred
from .findings_api_v1 import Finding
from .findings_api_v1 import FindingType
from .findings_api_v1 import Kpi
from .findings_api_v1 import KpiType
from .findings_api_v1 import NetworkConnection
from .findings_api_v1 import RemediationStep
from .findings_api_v1 import Reporter
from .findings_api_v1 import Section
from .findings_api_v1 import Severity
from .findings_api_v1 import SocketAddress
from .findings_api_v1 import ValueType
from .findings_api_v1 import ApiListNoteOccurrencesResponse
from .findings_api_v1 import ApiListNotesResponse
from .findings_api_v1 import ApiListOccurrencesResponse
from .findings_api_v1 import ApiListProvidersResponse
from .findings_api_v1 import ApiNote
from .findings_api_v1 import ApiNoteKind
from .findings_api_v1 import ApiNoteRelatedUrl
from .findings_api_v1 import ApiOccurrence
from .findings_api_v1 import ApiProvider
from .findings_api_v1 import BreakdownCardElement
from .findings_api_v1 import FindingCountValueType
#from .findings_api_v1 import KpiValueType
from .findings_api_v1 import NumericCardElement
from .findings_api_v1 import TimeSeriesCardElement

import warnings

warnings.warn("Depricated!!!!!!!!.   Use https://pypi.org/manage/project/ibm-cloud-security-advisor/releases/ instead of this package", DeprecationWarning)



