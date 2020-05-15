# Copyright (c) 2020 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# qumulo_python_versions = { 2, 3 }

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import qumulo.lib.opts
import qumulo.rest.replication as replication_rest

from qumulo.lib.opts import str_decode

def get_secret_access_key(secret_access_key):
    if secret_access_key is None:
        secret_access_key = qumulo.lib.opts.read_password(
            prompt="Enter secret access key associated with access key ID: ")

    return secret_access_key

class CreateObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_create_object_relationship"

    SYNOPSIS = """
    ==========================================================================
    EVALUATION USE ONLY. Please contact Qumulo Product Management for guidance
    ==========================================================================
    Create an object replication relationship that initiates a one-time copy of
    file data under the source directory to S3.
    """

    @staticmethod
    def options(parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--source-directory-id",
            type=str_decode,
            help="File ID of the source directory")
        group.add_argument(
            "--source-directory-path",
            type=str_decode,
            help="Path of the source directory")

        parser.add_argument(
            "--object-store-address",
            required=True,
            help="""S3-compatible server address, e.g.,
                s3.us-west-2.amazonaws.com""")

        parser.add_argument(
            "--object-folder",
            required=True,
            help="""Replication destination folder in the bucket. A slash
                separator is automatically used to create a "folder" in a
                bucket. For example, a folder of "example" and a file path
                (relative to source directory) of "dir/file" will result in key
                "example/dir/file". Use empty value "" or "/" to replicate to
                the root of the bucket.""")
        parser.add_argument(
            "--use-port",
            required=False,
            type=int,
            help="""HTTPS port to use when communicating with the object store
                (default: 443)""")
        parser.add_argument(
            "--ca-certificate",
            type=str_decode,
            help="""Path to a file containing the public certificate of the
                certificate authority to trust for connections to the object
                store, in PEM format. If not specified, the built-in trusted
                public CAs are used.""")
        parser.add_argument(
            "--bucket",
            required=True,
            help="Replication destination bucket in the object store")
        parser.add_argument(
            "--region", required=True, help="Region the bucket is located in")
        parser.add_argument(
            "--access-key-id",
            required=True,
            help="""Access key ID to use when communicating with the
                object store""")
        parser.add_argument(
            "--secret-access-key",
            help="""Secret access key to use when communicating with the
		object store""")

    @staticmethod
    def main(conninfo, credentials, args):
        secret_access_key = get_secret_access_key(args.secret_access_key)

        optional_args = {}

        if args.source_directory_id is not None:
            optional_args['source_directory_id'] = args.source_directory_id

        if args.source_directory_path is not None:
            optional_args['source_directory_path'] = args.source_directory_path

        if args.use_port is not None:
            optional_args['port'] = args.use_port

        if args.ca_certificate is not None:
            with open(args.ca_certificate) as f:
                optional_args['ca_certificate'] = f.read()

        print(replication_rest.create_object_relationship(
            conninfo,
            credentials,
            object_store_address=args.object_store_address,
            bucket=args.bucket,
            object_folder=args.object_folder,
            region=args.region,
            access_key_id=args.access_key_id,
            secret_access_key=secret_access_key,
            **optional_args))

class ListObjectRelationshipsCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_list_object_relationships"

    SYNOPSIS = "List all the existing object replication relationships."

    @staticmethod
    def main(conninfo, credentials, _args):
        print(replication_rest.list_object_relationships(
            conninfo, credentials))

class GetObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_get_object_relationship"

    SYNOPSIS = "Get configuration of the specified object replication "\
        "relationship."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", required=True,
            help="Unique identifier of the object replication relationship")

    @staticmethod
    def main(conninfo, credentials, args):
        print(replication_rest.get_object_relationship(
            conninfo, credentials, args.id))

class DeleteObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_delete_object_relationship"

    SYNOPSIS = "Delete the specified object replication relationship, "\
        "which must not be running a job."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", required=True,
            help="Unique identifier of the object replication relationship")

    @staticmethod
    def main(conninfo, credentials, args):
        replication_rest.delete_object_relationship(
            conninfo, credentials, args.id)

class AbortObjectReplicationCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_abort_object_replication"

    SYNOPSIS = "Abort ongoing replication for the specified object "\
        "replication relationship."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", required=True,
            help="Unique identifier of the object replication relationship")

    @staticmethod
    def main(conninfo, credentials, args):
        replication_rest.abort_object_replication(
            conninfo, credentials, args.id)

class ListObjectRelationshipStatusesCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_list_object_relationship_statuses"

    SYNOPSIS = "List the status for all existing object replication "\
        "relationships."

    @staticmethod
    def main(conninfo, credentials, _args):
        print(replication_rest.list_object_relationship_statuses(
            conninfo, credentials))

class GetObjectRelationshipStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = "replication_get_object_relationship_status"

    SYNOPSIS = "Get current status of the specified object replication "\
        "relationship."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", required=True,
            help="Unique identifier of the object replication relationship")

    @staticmethod
    def main(conninfo, credentials, args):
        print(replication_rest.get_object_relationship_status(
            conninfo, credentials, args.id))
