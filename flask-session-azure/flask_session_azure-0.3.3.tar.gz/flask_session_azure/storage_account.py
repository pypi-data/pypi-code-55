import base64

from Crypto.Cipher import AES
from azure.common import AzureMissingResourceHttpError
from azure.cosmosdb.table import TableService
from flask.json.tag import TaggedJSONSerializer


class StorageAccount(object):
    json_serializer = TaggedJSONSerializer()

    def __init__(self, connection_str: str, table_name: str, partition_key: str, create_table_if_not_exists: bool):
        self.table_name = table_name
        self.partition_key = partition_key
        self.create_table_if_not_exists = create_table_if_not_exists
        self.__table_service = TableService(connection_string=connection_str)

    def write(self, key: str, data: dict, encryption_key):
        """
        serializes and encrypts the passed dict object object and writes it to the storage
        """

        data = self.json_serializer.dumps(data)
        encoded_data, tag, nonce = self.encrypt(data, encryption_key)
        entity = {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            "Data": encoded_data,
            "Tag": tag,
            "Nonce": nonce
        }
        try:
            self.__table_service.insert_or_merge_entity(self.table_name, entity)
        except AzureMissingResourceHttpError:
            if not self.create_table_if_not_exists:
                raise
            self.__table_service.create_table(self.table_name)
            self.__table_service.insert_or_merge_entity(self.table_name, entity)

    def read(self, key: str, encryption_key: str):
        """
        reads encrypted data from storage and decrypts and deserializes it.
        Returns None if no data was found or decryption failed.
        """
        try:
            data = self.__table_service.get_entity(self.table_name, self.partition_key, key)
            decoded = self.decrypt(data["Data"], data["Tag"], data["Nonce"], encryption_key)
            if decoded is not None:
                return self.json_serializer.loads(decoded)
            return None
        except AzureMissingResourceHttpError:
            return None

    def delete(self, key: str):
        """
        Removes an element from storage if it exists
        """
        try:
            self.__table_service.delete_entity(self.table_name, self.partition_key, key)
        except AzureMissingResourceHttpError:
            pass

    @staticmethod
    def encrypt(data: str, secret_text: str):
        """
        encrypts the passed data with the secret text.
        :return: a tuple of three elements: encrypted data, verification_tag and nonce element.
        All elements are base64 encoded strings
        """
        cipher = AES.new(secret_text.encode("utf-8"), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest((data.encode("utf-8")))
        return (base64.b64encode(ciphertext).decode("ascii"),
                base64.b64encode(tag).decode("ascii"),
                base64.b64encode(cipher.nonce).decode("ascii"))

    @staticmethod
    def decrypt(encrypted_data: bytes, verification_tag: bytes, nonce: bytes, secret_text: str):
        """
        Decrypts encoded data using the passed secret_text
        :param encrypted_data:  as base64 encoded string or byte array
        :param verification_tag: as base64 encoded string or byte array
        :param nonce: as base64 encoded string or byte array
        :param secret_text: the same secret text with wich the element was encoded
        :return: the plaintext on success, None if the data could not be decoded or verified
        """
        nonce = base64.b64decode(nonce)
        cipher = AES.new(secret_text.encode("utf-8"), AES.MODE_EAX, nonce=nonce)
        data = base64.b64decode(encrypted_data)
        plaintext = cipher.decrypt(data)
        tag = base64.b64decode(verification_tag)
        try:
            cipher.verify(tag)
            return plaintext
        except ValueError:
            return None
