# coding: utf-8

"""

    No descripton provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems
import re


class ErrorSchemaExperiments(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, trace=None, errors=None):
        """
        ErrorSchemaExperiments - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'trace': 'str',
            'errors': 'list[ErrorExperiments]'
        }

        self.attribute_map = {
            'trace': 'trace',
            'errors': 'errors'
        }

        self._trace = trace
        self._errors = errors

    @property
    def trace(self):
        """
        Gets the trace of this ErrorSchemaExperiments.


        :return: The trace of this ErrorSchemaExperiments.
        :rtype: str
        """
        return self._trace

    @trace.setter
    def trace(self, trace):
        """
        Sets the trace of this ErrorSchemaExperiments.


        :param trace: The trace of this ErrorSchemaExperiments.
        :type: str
        """

        self._trace = trace

    @property
    def errors(self):
        """
        Gets the errors of this ErrorSchemaExperiments.


        :return: The errors of this ErrorSchemaExperiments.
        :rtype: list[ErrorExperiments]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """
        Sets the errors of this ErrorSchemaExperiments.


        :param errors: The errors of this ErrorSchemaExperiments.
        :type: list[ErrorExperiments]
        """

        self._errors = errors

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
