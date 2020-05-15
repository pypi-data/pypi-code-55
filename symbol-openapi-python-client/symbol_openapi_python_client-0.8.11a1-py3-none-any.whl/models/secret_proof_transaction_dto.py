# coding: utf-8

"""
    ****************************************************************************
    Copyright (c) 2016-present,
    Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp. All rights reserved.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
    ****************************************************************************
    
    Catapult REST Endpoints
    OpenAPI Specification of catapult-rest 1.0.20.34  # noqa: E501
    The version of the OpenAPI document: 0.8.10
    Contact: ravi@nem.foundation

    NOTE: This file is auto generated by Symbol OpenAPI Generator:
    https://github.com/nemtech/symbol-openapi-generator
    Do not edit this file manually.
"""


import pprint
import re  # noqa: F401

import six

from symbol_openapi_client.configuration import Configuration


class SecretProofTransactionDTO(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'signature': 'str',
        'signer_public_key': 'str',
        'version': 'int',
        'network': 'NetworkTypeEnum',
        'type': 'int',
        'max_fee': 'str',
        'deadline': 'str',
        'secret': 'str',
        'hash_algorithm': 'LockHashAlgorithmEnum',
        'recipient_address': 'str',
        'proof': 'str'
    }

    attribute_map = {
        'signature': 'signature',
        'signer_public_key': 'signerPublicKey',
        'version': 'version',
        'network': 'network',
        'type': 'type',
        'max_fee': 'maxFee',
        'deadline': 'deadline',
        'secret': 'secret',
        'hash_algorithm': 'hashAlgorithm',
        'recipient_address': 'recipientAddress',
        'proof': 'proof'
    }

    def __init__(self, signature=None, signer_public_key=None, version=None, network=None, type=None, max_fee=None, deadline=None, secret=None, hash_algorithm=None, recipient_address=None, proof=None, local_vars_configuration=None):  # noqa: E501
        """SecretProofTransactionDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._signature = None
        self._signer_public_key = None
        self._version = None
        self._network = None
        self._type = None
        self._max_fee = None
        self._deadline = None
        self._secret = None
        self._hash_algorithm = None
        self._recipient_address = None
        self._proof = None
        self.discriminator = None

        self.signature = signature
        self.signer_public_key = signer_public_key
        self.version = version
        self.network = network
        self.type = type
        self.max_fee = max_fee
        self.deadline = deadline
        self.secret = secret
        self.hash_algorithm = hash_algorithm
        self.recipient_address = recipient_address
        self.proof = proof

    @property
    def signature(self):
        """Gets the signature of this SecretProofTransactionDTO.  # noqa: E501

        Entity's signature generated by the signer.  # noqa: E501

        :return: The signature of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this SecretProofTransactionDTO.

        Entity's signature generated by the signer.  # noqa: E501

        :param signature: The signature of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and signature is None:  # noqa: E501
            raise ValueError("Invalid value for `signature`, must not be `None`")  # noqa: E501

        self._signature = signature

    @property
    def signer_public_key(self):
        """Gets the signer_public_key of this SecretProofTransactionDTO.  # noqa: E501

        Public key.  # noqa: E501

        :return: The signer_public_key of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._signer_public_key

    @signer_public_key.setter
    def signer_public_key(self, signer_public_key):
        """Sets the signer_public_key of this SecretProofTransactionDTO.

        Public key.  # noqa: E501

        :param signer_public_key: The signer_public_key of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and signer_public_key is None:  # noqa: E501
            raise ValueError("Invalid value for `signer_public_key`, must not be `None`")  # noqa: E501

        self._signer_public_key = signer_public_key

    @property
    def version(self):
        """Gets the version of this SecretProofTransactionDTO.  # noqa: E501

        Entity version.  # noqa: E501

        :return: The version of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this SecretProofTransactionDTO.

        Entity version.  # noqa: E501

        :param version: The version of this SecretProofTransactionDTO.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def network(self):
        """Gets the network of this SecretProofTransactionDTO.  # noqa: E501


        :return: The network of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: NetworkTypeEnum
        """
        return self._network

    @network.setter
    def network(self, network):
        """Sets the network of this SecretProofTransactionDTO.


        :param network: The network of this SecretProofTransactionDTO.  # noqa: E501
        :type: NetworkTypeEnum
        """
        if self.local_vars_configuration.client_side_validation and network is None:  # noqa: E501
            raise ValueError("Invalid value for `network`, must not be `None`")  # noqa: E501

        self._network = network

    @property
    def type(self):
        """Gets the type of this SecretProofTransactionDTO.  # noqa: E501


        :return: The type of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: int
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SecretProofTransactionDTO.


        :param type: The type of this SecretProofTransactionDTO.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def max_fee(self):
        """Gets the max_fee of this SecretProofTransactionDTO.  # noqa: E501

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :return: The max_fee of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._max_fee

    @max_fee.setter
    def max_fee(self, max_fee):
        """Sets the max_fee of this SecretProofTransactionDTO.

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :param max_fee: The max_fee of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and max_fee is None:  # noqa: E501
            raise ValueError("Invalid value for `max_fee`, must not be `None`")  # noqa: E501

        self._max_fee = max_fee

    @property
    def deadline(self):
        """Gets the deadline of this SecretProofTransactionDTO.  # noqa: E501

        Duration expressed in number of blocks.  # noqa: E501

        :return: The deadline of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        """Sets the deadline of this SecretProofTransactionDTO.

        Duration expressed in number of blocks.  # noqa: E501

        :param deadline: The deadline of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and deadline is None:  # noqa: E501
            raise ValueError("Invalid value for `deadline`, must not be `None`")  # noqa: E501

        self._deadline = deadline

    @property
    def secret(self):
        """Gets the secret of this SecretProofTransactionDTO.  # noqa: E501


        :return: The secret of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this SecretProofTransactionDTO.


        :param secret: The secret of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and secret is None:  # noqa: E501
            raise ValueError("Invalid value for `secret`, must not be `None`")  # noqa: E501

        self._secret = secret

    @property
    def hash_algorithm(self):
        """Gets the hash_algorithm of this SecretProofTransactionDTO.  # noqa: E501


        :return: The hash_algorithm of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: LockHashAlgorithmEnum
        """
        return self._hash_algorithm

    @hash_algorithm.setter
    def hash_algorithm(self, hash_algorithm):
        """Sets the hash_algorithm of this SecretProofTransactionDTO.


        :param hash_algorithm: The hash_algorithm of this SecretProofTransactionDTO.  # noqa: E501
        :type: LockHashAlgorithmEnum
        """
        if self.local_vars_configuration.client_side_validation and hash_algorithm is None:  # noqa: E501
            raise ValueError("Invalid value for `hash_algorithm`, must not be `None`")  # noqa: E501

        self._hash_algorithm = hash_algorithm

    @property
    def recipient_address(self):
        """Gets the recipient_address of this SecretProofTransactionDTO.  # noqa: E501

        Address expressed in hexadecimal base. If the bit 0 of byte 0 is not set (like in 0x90), then it is a regular address. Else (e.g. 0x91) it represents a namespace id which starts at byte 1.   # noqa: E501

        :return: The recipient_address of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._recipient_address

    @recipient_address.setter
    def recipient_address(self, recipient_address):
        """Sets the recipient_address of this SecretProofTransactionDTO.

        Address expressed in hexadecimal base. If the bit 0 of byte 0 is not set (like in 0x90), then it is a regular address. Else (e.g. 0x91) it represents a namespace id which starts at byte 1.   # noqa: E501

        :param recipient_address: The recipient_address of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and recipient_address is None:  # noqa: E501
            raise ValueError("Invalid value for `recipient_address`, must not be `None`")  # noqa: E501

        self._recipient_address = recipient_address

    @property
    def proof(self):
        """Gets the proof of this SecretProofTransactionDTO.  # noqa: E501

        Original random set of bytes.  # noqa: E501

        :return: The proof of this SecretProofTransactionDTO.  # noqa: E501
        :rtype: str
        """
        return self._proof

    @proof.setter
    def proof(self, proof):
        """Sets the proof of this SecretProofTransactionDTO.

        Original random set of bytes.  # noqa: E501

        :param proof: The proof of this SecretProofTransactionDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and proof is None:  # noqa: E501
            raise ValueError("Invalid value for `proof`, must not be `None`")  # noqa: E501

        self._proof = proof

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SecretProofTransactionDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SecretProofTransactionDTO):
            return True

        return self.to_dict() != other.to_dict()
