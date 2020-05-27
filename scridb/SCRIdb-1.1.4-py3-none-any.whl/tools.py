#!/usr/bin/env python3

import os
import sys
import re
import fnmatch
import shlex
import hashlib
import urllib.parse
import subprocess
import logging
from typing import Union, Tuple, Iterable, Optional
from collections import namedtuple, ChainMap

import json
import yaml
import boto3
import numpy as np
import pandas as pd

from .query import db_connect


def sample_fun(x: str) -> str:
    """\
    A function to return a new sample name omitting `IGO` part

    :param x:
        Old file name

    :return:
        New file name
    """
    if x.startswith("Sample_"):
        res = re.findall(r"(?<=_)(.*?)(?=_IGO)", x)
    elif "_IGO_" in x:
        res = re.findall(r"(.*?)(?=_IGO)", x)
    else:
        res = re.findall(r"(.*?)(?=_[Ss]\d{1,2}_|_L\d{3}_R\d_\d{3}.fastq.gz)", x)
    if res:
        return res[0]
    else:
        return x


def get_bucket_contents(root_source: str) -> list:
    """\
    List the contents of an object on `S3`.

    :param root_source:
        Parent directory on `S3`

    :return:
        List of objects in parent directory

    """
    s3 = boto3.client("s3")
    _, bucket, prefix, _, _ = urllib.parse.urlsplit(root_source)
    a = s3.list_objects(Bucket=bucket, Prefix=prefix.lstrip("/"))
    a = set([os.path.split(i["Key"])[-1] for i in a["Contents"]])
    a = [i for i in a if i]
    return a


def md5_checksum(filename: str) -> str:
    """\
    Compute the `MD5` digest of an object.

    :param filename:
        Path to file target file

    :return:
        `MD5` `hexdigest`
    """
    m = hashlib.md5()
    with open(filename, "rb") as f:
        for data in iter(lambda: f.read(1024 * 1024), b""):
            m.update(data)
    return m.hexdigest()


def etag_checksum(filename: str, chunk_size: int = 8 * 1024 * 1024) -> str:
    """\
    Compute the `ETag` digest (which is not the `MD5` digest) of an object.

    :param filename:
        Path to file target file
    :param chunk_size:
        Chunk size to hash

    :return:
        `ETag` `hexdigest`
    """
    md5s = []
    with open(filename, "rb") as f:
        for data in iter(lambda: f.read(chunk_size), b""):
            md5s.append(hashlib.md5(data).digest())
    m = hashlib.md5(b"".join(md5s))
    return "{}-{}".format(m.hexdigest(), len(md5s)) if len(md5s) > 1 else m.hexdigest()


def etag_compare(filename: str, etag: str) -> Tuple[bool, str, str]:
    """\
    Checks the integrity of files copied to `S3`.

    :param filename:
        Path to target file
    :param etag:
        `ETag` hash of `S3` object.

    :return:
        Checksum values of the object
    """
    et = etag.strip('"')
    if "-" in et:
        a = etag_checksum(filename)
    if "-" not in et:
        a = md5_checksum(filename)
    if et == a:
        return True, a, et

    return False, a, et


def get_cromwell_credentials(config: str = None) -> str:
    """\
    Return path to Cromwell server credentials. For new credentials it well attempt
    to create ones based on `user` and `password` from `config` file.

    :param config:
        Path to `config` file

    :return:
        Path to Cromwell credentials.
    """
    p = os.path.expanduser("~/.cromwell/credentials.json")
    if os.path.exists(p) and os.path.isfile(p):
        pass
    else:
        cred = json.load(open(config))
        os.makedirs(os.path.split(p)[0], mode=0o755, exist_ok=True)
        with open(p, "w") as f:
            json.dump(
                {
                    "url": "http://ec2-100-26-88-232.compute-1.amazonaws.com",
                    "username": cred["user"],
                    "password": cred["password"],
                },
                f,
                indent=4,
            )
            f.close()

    return p


def execute_cmd(cmd: str = None) -> tuple:
    """\
    Execute an external command.

    :param cmd:
        Command to be executed.

    :return:
        `STDOUT` and `STDERR` messages
    """
    p = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    n = False
    while True:
        out = p.stdout.readline()
        if out == b"" and p.poll() is not None:
            err = p.stderr.read()
            if p.poll() != 0:
                logging.error("Exit status %s while executing: %s", p.poll(), cmd)
            elif not n:
                err = "Empty response with exit status %s!!" % p.poll()
                err = err.encode()
                logging.warning("Empty response While executing: %s", cmd)
            break
        if out:
            print(out.decode().strip())
        n = True

    return out, err


def check_samples(x: Union[str, Iterable]) -> Iterable[int]:
    """\
    Check that records of sample exist in the database.

    :param x:
        Sample names.

    :return:
        Sample ids
    """
    if isinstance(x, str):
        x = [x]
    try:
        stmt1 = [
            (
                "SELECT sample_data.id "
                "FROM sample_data "
                "WHERE sample_data.Sample = '{}' COLLATE utf8mb4_bin".format(i)
            )
            for i in x
        ]
        stmt1 = "; ".join(stmt1)
        stmt2 = [
            (
                "SELECT "
                "concat('HTO_',hashtag_lib.sampleData_id) as 'HTO' "
                "FROM hashtag_lib "
                "WHERE hashtag_lib.Sample = '{}' COLLATE utf8mb4_bin".format(i)
            )
            for i in x
        ]
        stmt2 = "; ".join(stmt2)
        stmt3 = [
            (
                "SELECT "
                "concat('TCR_',TCR_lib.sampleData_id) as 'TCR' "
                "FROM TCR_lib "
                "WHERE TCR_lib.Sample = '{}' COLLATE utf8mb4_bin".format(i)
            )
            for i in x
        ]
        stmt3 = "; ".join(stmt3)

        stmt = "; ".join([stmt1, stmt2, stmt3])
        res = [
            (result.fetchall(), db_connect.cur.statement)
            for result in db_connect.cur.execute(stmt, multi=True)
        ]
        for i, s in res:
            if not i:
                print("NOT FOUND: ", s)
        print()
        res = [i[0] for i in res]
        if res:
            return [n[0][0] for n in res if n]
    except IndexError:
        sys.exit("Exit 1:\n\tSome or all the samples can't be found!")


def filter_samples(df: pd.DataFrame) -> Tuple[list, list]:
    """\
    To prevent accidental run on samples, for each sample in the data frame make sure:

    - it is on AWS
    - samples with hashtags are not being processed twice

    :param df:
        Data frame of samples

    :return:
        Filtered and excluded ids
    """
    filter_index, exclude_index = [], []
    for sample in df.itertuples():
        # search the database for a match to the following
        if sample.label == "sample_data":
            query = (
                "SELECT id FROM sample_data WHERE id={} and AWS_storage is "
                "NULL".format(sample.id)
            )
        else:
            query = (
                "SELECT sampleData_id FROM {} WHERE sampleData_id={} and "
                "AWS_storage is NULL".format(sample.label, sample.id)
            )
        db_connect.cur.execute(query)
        res = [i[0] for i in db_connect.cur.fetchall()]
        if res:
            logging.warning(str(res) + " " + db_connect.cur.statement)
            exclude_index.append(sample.Index)
        else:
            filter_index.append(sample.Index)

    return filter_index, exclude_index


def sample_data_frame(sd: pd.DataFrame) -> pd.DataFrame:
    """\
    Constructor for data frame with samples to be processed.

    :param sd:
        Data frame of fastq samples processed by `IGO` and transferred to `peerd` 
        drive. See example below.

    :return:
        A list of samples and other information from the database.

    Example
    =======

    >>> from SCRIdb.tools import *
    >>> db_connect.conn(os.path.expanduser("~/.config.json"))
    >>> f_in=[
                "Sample_CCR7_DC_1_IGO_10587_12",
                "Sample_CCR7_DC_2_IGO_10587_13",
                "Sample_CCR7_DC_3_IGO_10587_14",
                "Sample_CCR7_DC_4_IGO_10587_15"
        ]
    >>> f_in = " ".join(f_in)
    >>> source_path="/Volumes/peerd/FASTQ/Project_10587/MICHELLE_0194"
    >>> target_path="s3://dp-lab-data/sc-seq/Project_10587"
    >>> sd = pd.DataFrame(
            {
                "proj_folder": [source_path],
                "s3_loc": [target_path],
                "fastq": [f_in]
            }
        )
    >>> sample_data_frame(sd)
    """
    # it is assumed that every delivery of fastq files from the core are arranged in
    # subfolders as follows: project/subfolder/sample/
    sample_data = pd.DataFrame(
        columns=(
            "id",
            "sample",
            "project_id",
            "project_loc",
            "s3_loc",
            "genomeIndex_id",
            "species",
            "run_name",
            "barcodes",
            "genome_index",
            "insert_size",
            "old_basename",
            "label",
        )
    )
    for _, row in sd.iterrows():
        query = []
        row = dict(row)
        proj_folder = row["proj_folder"]
        s3_loc = row["s3_loc"]
        old_basename = row["fastq"].strip().split()
        print(old_basename)
        # extract sample names
        samples_ = [sample_fun(i) for i in old_basename]
        print(samples_)
        samples = np.array(samples_)
        # check if samples exist in the database and return their ids
        # if not, abort!
        id_sample = [i for i in map(check_samples, samples)]
        arr = np.array(id_sample)
        mask = arr.nonzero()[0]
        arr = np.concatenate(arr)
        not_found = np.setdiff1d(samples, samples[mask])
        if not_found.size != 0:
            msg = (
                "\n\n\t{:*^50s}\n".format(" START WARNING ")
                + "\n\n\tNo records where found for the following samples:\n"
                + "\n\n\t\t"
                + "\n\t\t".join(not_found)
                + "\n"
                + "\n\n\t{:*^50s}\n".format(" END WARNING ")
            )
            logging.warning(msg)
            samples = samples[mask]
        for s, o, id in zip(samples, np.array(old_basename)[mask], arr):
            if "HTO" in str(id):
                q = (
                    "SELECT "
                    "a.id, h.Sample, a.projectData_id, h.genomeIndex_id, "
                    "d.species, c.run_name, c.barcodes, b.gIndex, b.insert_size, "
                    "'{}' AS 'old_basename', 'HTO' as 'label' "
                    "FROM sample_data AS a "
                    "JOIN hashtag_lib AS h ON h.sampleData_id = a.id "
                    "JOIN genome_index AS b ON b.id = h.genomeIndex_id "
                    "JOIN sc_tech AS c ON c.id = b.scTech_id "
                    "JOIN species AS d ON d.id = b.species_id "
                    "WHERE a.id = '{}' AND h.Sample = '{}'".format(
                        o, id.lstrip("HTO_"), s
                    )
                )
                query.append(q)
            elif "TCR" in str(id):
                q = (
                    "SELECT "
                    "a.id, t.Sample, a.projectData_id, t.genomeIndex_id, "
                    "d.species, c.run_name, c.barcodes, b.gIndex, b.insert_size, "
                    "'{}' AS 'old_basename', 'TCR' as 'label' "
                    "FROM sample_data AS a "
                    "JOIN TCR_lib AS t ON t.sampleData_id = a.id "
                    "JOIN genome_index AS b ON b.id = t.genomeIndex_id "
                    "JOIN sc_tech AS c ON c.id = b.scTech_id "
                    "JOIN species AS d ON d.id = b.species_id "
                    "WHERE a.id = '{}' AND t.Sample = '{}'".format(
                        o, id.lstrip("TCR_"), s
                    )
                )
                query.append(q)
            else:
                q = (
                    "SELECT "
                    "a.id, a.Sample, a.projectData_id, a.genomeIndex_id, "
                    "d.species, c.run_name, c.barcodes, b.gIndex, b.insert_size, "
                    "'{}' AS 'old_basename', NULL as 'label' "
                    "FROM sample_data AS a "
                    "JOIN genome_index AS b ON b.id = a.genomeIndex_id "
                    "JOIN sc_tech AS c ON c.id = b.scTech_id "
                    "JOIN species AS d ON d.id = b.species_id "
                    "WHERE a.id = '{}' AND a.Sample = '{}'".format(o, id, s)
                )
                query.append(q)

        query_ = query
        query = "; ".join(query)
        res = [
            result.fetchall() for result in db_connect.cur.execute(query, multi=True)
        ]
        new_res = []
        for ele in res:
            if ele:
                new_res.append(ele[0])
        if not new_res:
            msg = (
                "\n\n\t{:*^50s}\n".format(" START WARNING ")
                + "\n\t{:.^50s}\n".format(" Empty Sample Data Frame ")
                + "\n\tThe following select statements failed:\n"
                + "\n\t\t"
                + query
                + "\n"
                + "\n\n\t{:*^50s}\n".format(" END WARNING ")
            )
            logging.warning(msg)
            sys.exit(
                "Warning:\n\tsample_data_frame: Empty. Check processing.log for "
                "errors and warnings!"
            )
        try:
            assert len(new_res) == samples.size, "Some critical data is missing!"
            res = np.hstack((new_res, [[proj_folder, s3_loc]] * len(samples)))
            sample_data = sample_data.append(
                pd.DataFrame(
                    res,
                    columns=[
                        "id",
                        "sample",
                        "project_id",
                        "genomeIndex_id",
                        "species",
                        "run_name",
                        "barcodes",
                        "genome_index",
                        "insert_size",
                        "old_basename",
                        "label",
                        "project_loc",
                        "s3_loc",
                    ],
                ),
                ignore_index=True,
                sort=False,
            )
        except AssertionError:
            res = np.hstack((new_res, [[proj_folder, s3_loc]] * len(new_res)))
            sample_data = sample_data.append(
                pd.DataFrame(
                    res,
                    columns=[
                        "id",
                        "sample",
                        "project_id",
                        "genomeIndex_id",
                        "species",
                        "run_name",
                        "barcodes",
                        "genome_index",
                        "insert_size",
                        "old_basename",
                        "label",
                        "project_loc",
                        "s3_loc",
                    ],
                ),
                ignore_index=True,
                sort=False,
            )

            excluded = np.setdiff1d(np.array(samples), res[:, 1])
            excluded = np.setdiff1d(excluded, not_found)
            st = np.array(query_)[
                np.isin([i.split()[-1].strip("'") for i in query_], excluded)
            ]
            msg = (
                "\n\n\t{:*^50s}\n".format(" START WARNING ")
                + "\n\tSome critical data is missing for the following samples:\n\n"
                + "\t\t"
                + "\n\t\t".join(excluded)
                + "\n\n\tThe following SELECT statements failed:\n\n\t\t"
                + "\n\t\t".join(st)
                + "\n\n\t{:*^50s}\n".format(" END WARNING ")
            )
            logging.warning(msg)

    table_dict = {"HTO": "hashtag_lib", "TCR": "TCR_lib", None: "sample_data"}
    sample_data["label"] = sample_data["label"].map(table_dict)
    return sample_data


def prepare_statements(sample_data: pd.DataFrame) -> dict:
    """\
    A constructor for `aws s3 cp` command and MySQL statements.

    :param sample_data:
        list of samples to be processed

    :return:
        A set of aws copy commands, and MySQL update commands
    """
    sample_set = {}
    for sample_ in sample_data.itertuples():
        cmd = []
        root_source = os.path.join(sample_.project_loc, sample_.old_basename, "")
        data_storage = os.path.join(sample_.s3_loc, sample_.sample, "")
        if sample_.label != "sample_data":
            whereid = "sampleData_id"
        else:
            whereid = "id"
        if sample_.label == "hashtag_lib":
            h_status = ", `status`=2"
        else:
            h_status = ""
        statement = (
            "UPDATE {} SET AWS_storage='{}', source_path='{}'{} WHERE {}="
            "{}".format(
                sample_.label, data_storage, root_source, h_status, whereid, sample_.id
            )
        )

        if root_source.startswith("s3://"):
            list_files = get_bucket_contents(root_source)
        else:
            list_files = os.listdir(root_source)

        for file in list_files:
            if sample_.run_name in [
                "ATAC",
                "H3",
                "H2",
                "H4",
                "VDJ",
                "five_prime",
                "CR",
            ] and fnmatch.fnmatch(file, "*.fastq.gz"):
                source_ = os.path.join(root_source, file)
                target_ = os.path.join(
                    data_storage, "FASTQ", "_".join([str(sample_.id), file])
                )

                _, bucket, key, _, _ = urllib.parse.urlsplit(target_)
                cmd.append([bucket, key.lstrip("/"), source_])

            else:
                if fnmatch.fnmatch(file, "*_R1_*.fastq.gz"):
                    target_filename = "_".join([str(sample_.id), file])
                    source_barcode = os.path.join(root_source, file)
                    target_barcode = os.path.join(
                        data_storage, "barcode", target_filename
                    )

                    _, bucket, key, _, _ = urllib.parse.urlsplit(target_barcode)
                    cmd.append([bucket, key.lstrip("/"), source_barcode])

                elif fnmatch.fnmatch(file, "*_R2_*.fastq.gz"):
                    target_filename = "_".join([str(sample_.id), file])
                    source_genomic = os.path.join(root_source, file)
                    target_genomic = os.path.join(
                        data_storage, "genomic", target_filename
                    )

                    _, bucket, key, _, _ = urllib.parse.urlsplit(target_genomic)
                    cmd.append([bucket, key.strip("/"), source_genomic])

        sample_set[str(sample_.id) + "_" + sample_.label] = dict(
            cmd=cmd, statement=statement
        )

    return sample_set


def put_object(
    dest_bucket_name: str,
    dest_object_name: str,
    src_data: str,
    md5sums: Optional[Union[str, dict]] = None,
) -> Tuple[str, bool]:
    """\
    Put an object on Amazon S3 bucket, while verifying the integrity of the uploaded
    object.

    .. note::
        More information on how to verify the integrity of the uploaded
        object using `ETag` and `MD5` can be found here_.

    .. _here: https://aws.amazon.com/premiumsupport/knowledge-center/data-integrity-s3/

    :param dest_bucket_name:
        Bucket name
    :param dest_object_name:
        Target `S3` key
    :param src_data:
        Path to source file
    :param md5sums:
        A set of key (name), value (MD5 hash) or path to MD5 hashes file

    :return:
        `tuple`
    """

    print("*** Uploading {} ...".format(os.path.basename(src_data)))
    target_path = os.path.join("s3://", dest_bucket_name, dest_object_name)
    cmd = f"aws s3 cp {src_data} {target_path}"

    out, err = execute_cmd(cmd)
    if err:
        logging.error(
            "Failed to add %s to %s!!",
            os.path.basename(dest_object_name),
            os.path.dirname(dest_object_name),
        )
        return err, False

    # check for integrity
    obj = boto3.resource("s3").Object(dest_bucket_name, dest_object_name)
    if md5sums:
        if isinstance(md5sums, str) and os.path.isfile(md5sums):
            with open(md5sums, "r") as f:
                md5_hashes = {n[1]: n[0] for n in [i.split() for i in f.readlines()]}
        else:
            try:
                assert isinstance(md5sums, dict), (
                    "AssertionError: `md5sums` must be "
                    "a valid file name or a set of key "
                    "(name), value (MD5 hash)!"
                )
                md5_hashes = md5sums
            except AssertionError as e:
                print(str(e))
                return b"Checksum failed", False
        if obj.e_tag == md5_hashes[os.path.basename(src_data)]:
            logging.info(
                "--- Added %s to %s",
                os.path.basename(dest_object_name),
                os.path.dirname(dest_object_name),
            )
            return b"", True
        else:
            logging.error(
                "Checksum failed %s (%s) to %s (%s)!!",
                src_data,
                md5_hashes[os.path.basename(src_data)],
                dest_object_name,
                obj.e_tag,
            )
            return b"Checksum failed", False
    else:
        checksum, atag, etag = etag_compare(src_data, obj.e_tag)
        if not checksum:
            logging.error(
                "Checksum failed %s (%s) to %s (%s)!!",
                src_data,
                atag,
                dest_object_name,
                etag,
            )
            return b"Checksum failed", checksum
        else:
            logging.info(
                "--- Added %s to %s",
                os.path.basename(dest_object_name),
                os.path.dirname(dest_object_name),
            )
            return b"", True


class JobsYmlKeys:
    def __init__(self, email: str = None, n: int = 1, seqcargs=None, **kargs):

        self.email = email
        self.seqcargs = seqcargs
        self.n = n
        self.kargs = kargs
        self.appropriate_case = self.kargs["run_name"]

    @classmethod
    def classic(
        cls,
        ami: str = None,
        instance_type: str = None,
        star_args: str = None,
        email: str = None,
        n: int = None,
        seqcargs=None,
        **kargs,
    ):

        keywords = [
            "job",
            "ami-id",
            "platform",
            "user-tags",
            "index",
            "barcode-files",
            "genomic-fastq",
            "barcode-fastq",
            "upload-prefix",
            "output-prefix",
            "email",
            "star-args",
            "instance-type",
        ]

        Classicyml = namedtuple(
            "Classicyml",
            ["job", "ami_id", "user_tags", "instance_type", "star_args"]
            + list(kargs.keys())
            + ["email"]
            if email
            else [],
        )
        clayml = Classicyml(
            job=n,
            ami_id=ami,
            user_tags={"jobs": n},
            instance_type=instance_type,
            star_args=star_args,
            email=email,
            **kargs,
        )

        claymldict = ChainMap(clayml._asdict())
        claymldict["ami-id"] = claymldict.pop("ami_id")
        claymldict["platform"] = claymldict.pop("run_name")
        claymldict["user-tags"] = claymldict.pop("user_tags")
        claymldict["user-tags"]["projectId"] = claymldict.pop("project_id")
        sampleName = re.search(
            f"{claymldict['sample']}.*", claymldict.pop("old_basename")
        )
        sampleName = "_".join([str(claymldict.pop("id")), sampleName.group()])
        claymldict["user-tags"]["sampleName"] = sampleName
        claymldict["index"] = claymldict.pop("genome_index")
        claymldict["barcode-files"] = claymldict.pop("barcodes")
        path = os.path.join(
            claymldict.pop("s3_loc"), claymldict.pop("sample"), "{}", ""
        )
        claymldict["genomic-fastq"] = path.format("genomic")
        claymldict["barcode-fastq"] = path.format("barcode")
        claymldict["upload-prefix"] = path.format("seqc-results")
        claymldict["output-prefix"] = sampleName
        claymldict["star-args"] = claymldict.pop("star_args")
        claymldict["instance-type"] = claymldict.pop("instance_type")

        # for all snRNA-seq set parameters "filter-mode" and "max-insert-size"
        sql = (
            "SELECT genome_index.id FROM genome_index LEFT JOIN sc_tech ON "
            "sc_tech.id = genome_index.scTech_id "
            "WHERE sc_tech.sc_Tech LIKE '%snRNA-seq'"
        )
        db_connect.cur.execute(sql)
        res = [i[0] for i in db_connect.cur.fetchall()]
        if int(claymldict["genomeIndex_id"]) in res:
            claymldict["filter-mode"] = "snRNA-seq"
            claymldict["max-insert-size"] = claymldict.pop("insert_size")
            [keywords.append(i) for i in ["filter-mode", "max-insert-size"]]

        # for all indrops set parameter "no-filter-low-coverage"
        sql = (
            "SELECT genome_index.id FROM genome_index LEFT JOIN sc_tech ON "
            "sc_tech.id = genome_index.scTech_id "
            "WHERE sc_tech.Run_Name LIKE 'in_drop%'"
        )
        db_connect.cur.execute(sql)
        res = [i[0] for i in db_connect.cur.fetchall()]
        if int(claymldict["genomeIndex_id"]) in res:
            claymldict["no-filter-low-coverage"] = ""
            keywords.append("no-filter-low-coverage")

        yamlDict = {i: claymldict[i] for i in keywords}

        # pass additional SEQC arguments to Yaml
        if seqcargs:
            for k, v in seqcargs.items():
                yamlDict[k] = v

        return yamlDict

    @classmethod
    def CR(cls, mode: str = None, n: int = None, **kargs):

        keywords = [
            "job",
            "projectId",
            "sampleName",
            "referenceTranscriptome",
            "uriS3Fastq",
            "uriS3Output",
        ]
        Classicyml = namedtuple("Classicyml", ["job"] + list(kargs.keys()))
        clayml = Classicyml(job=n, **kargs)
        claymldict = ChainMap(clayml._asdict())
        claymldict["projectId"] = str(claymldict.pop("project_id"))
        sampleName = re.search(
            f"{claymldict['sample']}.+", claymldict.pop("old_basename")
        )
        sampleName = "_".join([str(claymldict.pop("id")), sampleName.group()])
        claymldict["sampleName"] = sampleName
        claymldict["referenceTranscriptome"] = claymldict.pop("genome_index")
        path = os.path.join(
            claymldict.pop("s3_loc"), claymldict.pop("sample"), "{}", ""
        )
        claymldict["uriS3Fastq"] = path.format("FASTQ")
        claymldict["uriS3Output"] = path.format("CR-results")
        if mode == "atac":
            claymldict["processPeaks"] = {
                "peakMergeDistance": 10,
                "significanceLevel": 0.01,
            }
            claymldict["referenceGenome"] = claymldict.pop("referenceTranscriptome")
            keywords.append("processPeaks")
            keywords = [
                i
                for i in keywords + ["referenceGenome"]
                if i != "referenceTranscriptome"
            ]

        return {i: claymldict[i] for i in keywords}

    @classmethod
    def hashtags(cls, **kargs):

        from SCRIdb.upload_stats import get_objects

        j_hash = [
            "Sharp.uriFastqR1",
            "Sharp.uriFastqR2",
            "Sharp.sampleName",
            "Sharp.scRnaSeqPlatform",
            "Sharp.lengthR1",
            "Sharp.lengthR2",
            "Sharp.cellBarcodeWhitelistUri",
            "Sharp.cellBarcodeWhiteListMethod",
            "Sharp.hashTagList",
            "Sharp.cbStartPos",
            "Sharp.cbEndPos",
            "Sharp.umiStartPos",
            "Sharp.umiEndPos",
            "Sharp.trimPos",
            "Sharp.slidingWindowSearch",
            "Sharp.cbCollapsingDistance",
            "Sharp.umiCollapsingDistance",
            "Sharp.numExpectedCells",
            "Sharp.numCoresForCount",
            "Sharp.denseCountMatrix",
        ]
        j_labels = [
            "pipelineType",
            "project",
            "sample",
            "owner",
            "destination",
            "transfer",
            "comment",
        ]

        Classicyml = namedtuple("Classicyml", list(kargs.keys()))
        clayml = Classicyml(**kargs)
        claymldict = ChainMap(clayml._asdict())

        # before attempting any compiling of json check if a dense matrix exists and
        # can be used
        stmt = (
            "SELECT stats_data.analysis_storage, barcodes "
            "FROM sample_data "
            "LEFT JOIN stats_data ON stats_data.sampleData_id = sample_data.id "
            "LEFT JOIN hashtag_lib ON hashtag_lib.sampleData_id = sample_data.id "
            "LEFT JOIN genome_index ON genome_index.id = "
            "hashtag_lib.genomeIndex_id "
            "LEFT JOIN sc_tech ON sc_tech.id = genome_index.scTech_id "
            "WHERE sample_data.id = {}".format(claymldict["id"])
        )
        db_connect.cur.execute(stmt)
        dm_parent, barcodes = [i for i in db_connect.cur.fetchall()][0]
        try:
            assert (
                dm_parent
            ), "Empty `analysis_storage` in SELECT statement:\n\t{}".format(
                db_connect.cur.statement
            )
            _, bucket, key, _, _ = urllib.parse.urlsplit(dm_parent)
            dm = get_objects(bucket, key.strip("/"), re.compile("_dense.csv$"))
            try:
                dm = os.path.join("s3://", bucket, dm[0])
            except IndexError:
                logging.error(
                    "Path to cell x gene dense matrix of genomic data is missing!"
                    "\n\t{}".format(db_connect.cur.statement)
                )
                return
        except AssertionError:
            logging.warning("Path to genomic output results is missing!")
            return

        path = os.path.join(claymldict.pop("s3_loc"), claymldict["sample"], "")
        _, bucket, key, _, _ = urllib.parse.urlsplit(path)
        R1 = get_objects(bucket, key.strip("/"), re.compile("_R1_\d\d\d.fastq.gz$"))
        R1 = [os.path.join("s3://", bucket, i) for i in R1]
        R2 = get_objects(bucket, key.strip("/"), re.compile("_R2_\d\d\d.fastq.gz$"))
        R2 = [os.path.join("s3://", bucket, i) for i in R2]

        try:
            assert R1
            assert R2
        except AssertionError:
            logging.warning("uriFastqR1/2 Empty:\n\t %s", path)
            return str(claymldict["id"])

        barcodes = json.loads(barcodes)
        cb = barcodes["cellbarcode"]
        umi = cb + barcodes["UMIs"]

        stmt = (
            "SELECT barcode_sequence, concat(substring(category, -1), barcode), "
            "demultiplex_label, bp_shift FROM hashtags "
            "LEFT JOIN "
            "hashtag_barcodes ON hashtag_barcodes.id = hashtags.hashtagBarcodes_id "
            "WHERE sampleData_id = {}".format(claymldict["id"])
        )
        db_connect.cur.execute(stmt)
        res = db_connect.cur.fetchall()
        hres = all([all(i[:2]) for i in res])
        if not hres:
            logging.warning("Barcodes data Empty:\n\t %s", db_connect.cur.statement)
            return str(claymldict["id"])
        hres = pd.DataFrame(res, columns=["sequence", "code", "label", "bp_shift"])
        seq_length = list(set(map(len, hres.sequence)))
        if len(seq_length) > 1:
            seq_length = max(seq_length)
        else:
            seq_length = seq_length[0]

        if hres.bp_shift.unique().size != 1:
            logging.warning(
                "sample {} {} has hash tag barcode categories, "
                "with bp-shift length/s {}, and will not be processed!".format(
                    claymldict["id"], claymldict["sample"], hres.bp_shift.unique()
                )
            )
            return str(claymldict["id"])
        else:
            claymldict["Sharp.trimPos"] = int(hres.bp_shift.unique()[0])

        seq_length = seq_length + claymldict["Sharp.trimPos"]

        claymldict["pipelineType"] = "Sharp"
        claymldict["owner"] = os.getlogin()
        claymldict["transfer"] = "-"
        claymldict["comment"] = "Hashtag Pipeline"

        claymldict["project"] = "Project {}".format(claymldict["project_id"])
        claymldict["sample"] = "_".join([str(claymldict["id"]), claymldict["sample"]])
        claymldict["destination"] = os.path.join(path, "Hashtag_results", "")
        claymldict["Sharp.scRnaSeqPlatform"] = {
            "H2": "10x_v2",
            "H3": "10x_v3",
            "H4": "in_drop_v4",
        }[claymldict["run_name"]]
        claymldict["Sharp.slidingWindowSearch"] = False

        claymldict["Sharp.cbStartPos"] = 1
        claymldict["Sharp.cbCollapsingDistance"] = 1
        claymldict["Sharp.umiCollapsingDistance"] = 1
        claymldict["Sharp.numExpectedCells"] = 0
        claymldict["Sharp.numCoresForCount"] = 8
        claymldict["Sharp.cellBarcodeWhiteListMethod"] = "SeqcDenseCountsMatrixCsv"

        claymldict["Sharp.uriFastqR1"] = R1
        claymldict["Sharp.uriFastqR2"] = R2
        claymldict["Sharp.sampleName"] = claymldict["sample"]
        claymldict["Sharp.lengthR1"] = umi
        claymldict["Sharp.lengthR2"] = seq_length
        claymldict["Sharp.cellBarcodeWhitelistUri"] = dm
        claymldict["Sharp.hashTagList"] = os.path.join(
            claymldict["destination"], "tag-list.csv"
        )
        claymldict["Sharp.cbEndPos"] = cb
        claymldict["Sharp.umiStartPos"] = cb + 1
        claymldict["Sharp.umiEndPos"] = umi
        claymldict["Sharp.denseCountMatrix"] = dm
        claymldict["Sharp.cbEndPos"] = cb

        inputs = os.path.join("config", "{}.inputs.json".format(claymldict["sample"]))
        labels = os.path.join("config", "{}.labels.json".format(claymldict["sample"]))

        sets = ChainMap(
            {i: claymldict[i] for i in j_hash},
            {i: claymldict[i] for i in j_labels},
            {
                "inputs": inputs,
                "labels": labels,
                "tag_list": claymldict["Sharp.hashTagList"],
                "hres": hres,
            },
        )

        return sets

    @property
    def appropriate_case(self) -> tuple:
        return self.__appropriatecase

    @appropriate_case.setter
    def appropriate_case(self, mode):
        if mode.lower() not in [
            i.lower() for i in ["ATAC", "H3", "H2", "H4", "VDJ", "five_prime", "CR"]
        ]:
            self.__appropriatecase = self.classic(
                email=self.email, n=self.n, seqcargs=self.seqcargs, **self.kargs,
            )
        elif mode.lower() in [i.lower() for i in ["ATAC", "five_prime", "CR"]]:
            self.__appropriatecase = self.CR(mode=mode.lower(), n=self.n, **self.kargs)
        elif mode.lower() in [i.lower() for i in ["H3", "H2", "H4"]]:
            self.__appropriatecase = self.hashtags(**self.kargs)
        else:
            self.__appropriatecase = mode


def jobs_yml_config(
    sample_data: pd.DataFrame,
    config_jobs_yml: str = None,
    ami: str = "ami-0a4d2955fe21dee72",
    instance_type: str = "r5.2xlarge",
    star_args: str = "runRNGseed=0",
    email: str = None,
    seqcargs=None,
) -> None:
    """\
    Constructor for `yaml` formatted file for batch processing of samples.

    :param sample_data:
        Data frame of samples to be processed, generated by this function
        :func:`~.SCRIdb.tools.sample_data_frame`
    :param config_jobs_yml:
        Path to output `.yml` file in `config` directory for batch processing
    :param ami:
        SEQC AMI (Amazon Machine Image) to use
    :param instance_type:
        EC2 instance type to be used
    :param star_args:
        Arguments passed to the `STAR` aligner.
    :param email:
        Email address to receive run summary or errors when running remotely.
        Optional only if running locally.
    :param seqcargs:
        Additional arguments passed to seqc

    :return:
        `None`

    Example
    =======

    >>> from SCRIdb.worker import *
    >>> args = json.load(open(os.path.expanduser("~/.config.json")))
    >>> args["jobs"] = "jobs.yml"
    >>> args["seqcargs"] = {"min-poly-t": 0}
    >>> db_connect.conn(args)

    >>> f_in=[
                "Sample_CCR7_DC_1_IGO_10587_12",
                "Sample_CCR7_DC_2_IGO_10587_13",
                "Sample_CCR7_DC_3_IGO_10587_14",
                "Sample_CCR7_DC_4_IGO_10587_15"
        ]
    >>> f_in = " ".join(f_in)
    >>> source_path="/Volumes/peerd/FASTQ/Project_10587/MICHELLE_0194"
    >>> target_path="s3://dp-lab-data/sc-seq/Project_10587"
    >>> sd = pd.DataFrame(
            {
                "proj_folder": [source_path],
                "s3_loc": [target_path],
                "fastq": [f_in]
            }
        )
    >>> sample_data = sample_data_frame(sd)
    >>> jobs_yml_config(
            sample_data,
            email=args["email"],
            config_jobs_yml=os.path.join(args["dockerizedSEQC"], "config",
            args["jobs"]),
            seqcargs=args["seqcargs"],
        )
    """
    jobs = {"jobs": []}
    n = 0
    for sample_ in sample_data.itertuples():
        n += 1
        if sample_.run_name in ["ten_x_v3", "ten_x_v2"]:
            seqcargs_ = ChainMap(seqcargs, {"min-poly-t": "0"})
            try:
                seqcargs_ = dict(seqcargs_)
            except TypeError:
                seqcargs_ = {"min-poly-t": "0"}
        else:
            seqcargs_ = seqcargs
        jobs_yml_ = JobsYmlKeys(
            ami=ami,
            star_args=star_args,
            instance_type=instance_type,
            email=email,
            n=n,
            seqcargs=seqcargs_,
            **sample_._asdict(),
        )

        jobs["jobs"].append(jobs_yml_.appropriate_case)

    try:
        assert os.path.isdir(os.path.dirname(config_jobs_yml)), ""
        print("Jobs YAML file will be written to:\n\t\t {}".format(config_jobs_yml))
    except AssertionError:
        print("{:*^80}".format(" WARNING "))
        logging.warning(
            "{:>10}Path `{}` does not exist!".format(
                "", os.path.dirname(config_jobs_yml)
            )
        )
        logging.warning(
            "{:>10}Try using `--tool_path [TOOL_PATH]` to override the "
            "default path to your tool.".format("")
        )
        config_jobs_yml = os.path.join(
            os.path.expanduser("~"), os.path.basename(config_jobs_yml)
        )
        logging.warning(
            "{:>10}Jobs YAML will be saved to `{}`!".format("", config_jobs_yml)
        )

    print()
    yaml.dump(jobs, open(config_jobs_yml, "w"), sort_keys=False)

    return None


def json_hasttags(sample_data: pd.DataFrame, config_path) -> list:
    """\
    Constructor for `json` formatted files for batch processing of hashtag samples.
    It Compiles `input` and `label` files for each sample in the provided data frame.

    :param sample_data:
        Data frame of samples to be processed
    :param config_path:
        Path to root directory of hashtag pipeline executable `submit.sh`. It also
        serves as the parent directory for `config` where `.json` files will be written.

    :return:
        Inputs, labels, and a list of excluded samples

    Example
    =======

    >>> from SCRIdb.worker import *
    >>> args = json.load(open(os.path.expanduser("~/.config.json")))
    >>> db_connect.conn(args)

    >>> f_in=[
                "Sample_CCR7_DC_1_HTO_IGO_10587_12",
                "Sample_CCR7_DC_2_HTO_IGO_10587_13",
                "Sample_CCR7_DC_3_HTO_IGO_10587_14",
                "Sample_CCR7_DC_4_HTO_IGO_10587_15"
        ]
    >>> f_in = " ".join(f_in)
    >>> source_path="/Volumes/peerd/FASTQ/Project_10587/MICHELLE_0194"
    >>> target_path="s3://dp-lab-data/sc-seq/Project_10587"
    >>> sd = pd.DataFrame(
            {
                "proj_folder": [source_path],
                "s3_loc": [target_path],
                "fastq": [f_in]
            }
        )
    >>> sample_data = sample_data_frame(sd)
    >>> inputs_labels, exclude_s = json_hasttags(
            sample_data,
            config_path=os.path.expanduser("~/sharp-0.0.1"),
        )
    """
    inputs_, labels_, exclude_ = [], [], []
    for sample in sample_data.itertuples():
        jobs_json = JobsYmlKeys(**sample._asdict())
        if isinstance(jobs_json.appropriate_case, str):
            exclude_.append(jobs_json.appropriate_case)
        elif jobs_json.appropriate_case:
            j_hash = jobs_json.appropriate_case.maps[0]
            j_labels = jobs_json.appropriate_case.maps[1]
            inputs = jobs_json.appropriate_case["inputs"]
            labels = jobs_json.appropriate_case["labels"]
            with open(os.path.join(config_path, inputs), "w") as f:
                f.write(json.dumps(j_hash, indent=4))
                f.close()
            with open(os.path.join(config_path, labels), "w") as f:
                f.write(json.dumps(j_labels, indent=4))
                f.close()
            print(
                "Inputs and labels json files were written to:\n\t\t {}".format(
                    os.path.join(config_path, "config")
                )
            )
            # write tag-list to AWS
            hres = jobs_json.appropriate_case["hres"]
            tag_list = jobs_json.appropriate_case["tag_list"]
            f = hres.to_csv(header=False, index=False)
            s3 = boto3.resource("s3")
            _, bucket, key, _, _ = urllib.parse.urlsplit(tag_list)
            obj = s3.Object(bucket, key.strip("/"))
            obj.put(Body=f.encode())

            inputs_.append(inputs)
            labels_.append(labels)

    return [zip(inputs_, labels_), exclude_]
