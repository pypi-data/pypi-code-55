#!/usr/bin/env python3

import datetime
from datetime import date

import mysql

from .query import run
from .tools import *


def worker_main(
    f_in: Union[str, list],
    source_path: str = None,
    target_path: str = None,
    runseqc: bool = True,
    hashtag: bool = True,
    atac: bool = True,
    CR: bool = True,
    no_rsync: bool = False,
    save: bool = False,
    **args
) -> None:
    """\
    A method to process raw sequencing data returned from **IGO**. Newly sequenced
    samples are copied from IGO shared drive to a defined `S3URI`. Then, the proper
    pipeline is called to process the copied raw data.

    :param f_in:
        Input file name, a single sample name, or a list of sample names, sequenced and
        ready to be processed
    :param source_path:
        Source path to parent directory of sequenced samples, usually an IGO shared
        drive
    :param target_path:
        Target path to parent directory of sequenced samples, usually, a `S3URI`
    :param no_rsync:
        Skip copying files to `S3`
    :param runseqc:
        Call `seqc` pipeline
    :param hashtag:
        Call `hashtag` pipeline
    :param atac:
        Call `atac-seq` pipeline
    :param CR:
        Call `Cell Ranger` pipeline
    :param save:
        Write `sample_data` to `.csv` output configured in `--results_output`
    :param args:
        Additional args passed to other methods

    :return:
        `None`

    Example
    =======

    >>> from SCRIdb.worker import *
    >>> args = json.load(open(os.path.expanduser("~/.config.json")))
    >>> args["jobs"] = "jobs.yml"
    >>> args["seqcargs"] = {"min-poly-t": 0}
    >>> db_connect.conn(args)
    >>> worker_main(
        f_in=[
                "Sample_CCR7_DC_1_IGO_10587_12",
                "Sample_CCR7_DC_2_IGO_10587_13",
                "Sample_CCR7_DC_3_IGO_10587_14",
                "Sample_CCR7_DC_4_IGO_10587_15"
        ],
        source_path="/Volumes/peerd/FASTQ/Project_10587/MICHELLE_0194",
        target_path="s3://dp-lab-data/sc-seq/Project_10587",
        runseqc = False,
        no_rsync = True,
        **args
    )
    """

    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(asctime)s: %(message)s")

    fh = logging.FileHandler("processing.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    print("Processing new fastq files ...")

    # read in delivery report
    if isinstance(f_in, list):
        f_in = " ".join(f_in)
    if os.path.isfile(f_in):
        sd = pd.read_csv(f_in, index_col=0)
    else:
        if any([source_path is None, target_path is None]):
            print("WARNING: Missing at least one of source_path and target_path!")
            return
        sd = pd.DataFrame(
            {"proj_folder": [source_path], "s3_loc": [target_path], "fastq": [f_in]}
        )

    sample_data = sample_data_frame(sd)

    failed_samples = []
    if not no_rsync:
        # copy fastq files, rename the samples, and update the database
        sample_set = prepare_statements(sample_data)
        for key in sample_set:
            success_list = []
            for cmd in sample_set[key]["cmd"]:
                dest_bucket_name, dest_object_name, src_data = cmd
                msg, success = put_object(
                    dest_bucket_name, dest_object_name, src_data, args["md5sums"]
                )
                if success:
                    success_list.append(success)
                else:
                    # logging.error('%s', msg.decode())
                    failed_samples.append(str(key))
            if all(success_list):
                # check if important_dates has valid IGO_sub_date and sequencing_date
                db_connect.cur.execute(
                    "SELECT IGO_sub_date, sequencing_date FROM important_dates "
                    "WHERE sampleData_id = %s",
                    (key.split("_")[0],),
                )
                res = db_connect.cur.fetchall()
                if res:
                    for i in zip(["IGO_sub_date", "sequencing_date"], res[0]):
                        if not isinstance(i[1], datetime.date):
                            stmt = (
                                "UPDATE important_dates SET {}='{}' WHERE "
                                "sampleData_id={}".format(
                                    i[0],
                                    date.fromtimestamp(os.path.getatime(src_data)),
                                    key.split("_")[0],
                                )
                            )
                            db_connect.cur.execute(stmt)
                            print(db_connect.cur.statement)
                    try:
                        db_connect.cur.execute(sample_set[key]["statement"])
                        print(db_connect.cur.statement)
                    except mysql.connector.Error as err:
                        print(
                            "Something went wrong with sample {}: {}".format(
                                key.split("_")[0], err
                            )
                        )
                        db_connect.db.rollback()
                    finally:
                        db_connect.db.commit()
                else:
                    print(
                        "No records found for sample {}:\n\t{}".format(
                            key.split("_")[0], db_connect.cur.statement
                        )
                    )
                    logging.warning(
                        "Sample '{}' will be excluded from processing!".format(
                            key.split("_")[0]
                        )
                    )
                    failed_samples.append(str(key.split("_")[0]))

    # write the processing jobs to yaml
    # need to determine `run_name` to build proper yaml files
    # don't include failed-to-transfer samples
    filter_index, exclude_index = filter_samples(sample_data)
    if exclude_index:
        logging.warning(
            "Samples {} will be excluded from processing due to missing "
            "meta data!".format(sample_data.id[exclude_index].tolist())
        )
    sample_data = sample_data.iloc[filter_index]

    criterion = sample_data["id"].map(lambda x: str(x) not in failed_samples)
    sample_data_ = sample_data[criterion]

    if sample_data_.empty:
        print("\nSample data frame is empty! Nothing to process!...\n")
        print("{:-^50}\n".format(" END "))

        return

    idx_seqc = sample_data_["run_name"].map(
        lambda x: x not in ["ATAC", "H3", "H2", "H4", "VDJ", "five_prime", "CR"]
    )
    idx_atac = sample_data_["run_name"].map(lambda x: x == "ATAC")
    idx_hashtag = sample_data_["run_name"].map(lambda x: x in ["H3", "H2", "H4"])
    idx_cellranger = sample_data_["run_name"].map(lambda x: x in ["five_prime", "CR"])
    idx_vdj = sample_data_["run_name"].map(lambda x: x == "VDJ")

    if idx_seqc.any():
        config_jobs_yml = os.path.join(args["dockerizedSEQC"], "config", args["jobs"])
        jobs_yml_config(
            sample_data_[idx_seqc],
            email=args["email"],
            config_jobs_yml=config_jobs_yml,
            seqcargs=args["seqcargs"],
        )

        if runseqc:
            run(execp="seqc_submit_mjobs.py", path=args["dockerizedSEQC"], **args)

    if idx_atac.any():
        path = (
            args["tool_path"]
            if args["tool_path"]
            else os.path.join(os.path.expanduser("~"), "scata")
        )
        config_jobs_yml = os.path.join(path, "config", args["jobs"])
        jobs_yml_config(
            sample_data_[idx_atac],
            email=args["email"],
            config_jobs_yml=config_jobs_yml,
        )

        if atac:
            run(execp="scata_submit_mjobs.py", path=path, **args)

    if idx_hashtag.any():
        path = (
            args["tool_path"]
            if args["tool_path"]
            else os.path.join(os.path.expanduser("~"), "sharp-0.0.1")
        )
        hsample_data = sample_data_[idx_hashtag]
        inputs_labels, exclude_s = json_hasttags(hsample_data, config_path=path)

        print("Excluding:", exclude_s)
        filter_excluded = sample_data_["id"].map(lambda x: str(x) not in exclude_s)
        sample_data_ = sample_data_[filter_excluded]

        if hashtag:
            # generate a secret key for cromwell server if not found in path
            secret_cromwell = get_cromwell_credentials(db_connect.config)
            print("Establishing connection to Ceomwell Server, please wait ...!")
            for inputs, labels in inputs_labels:
                kargs = {"inputs": inputs, "labels": labels, "secret": secret_cromwell}
                try:
                    run(execp="./submit.sh", path=path, hashtag_param=kargs, **args)
                    print(inputs, labels, "successfully deployed to Cromwell!")
                    label_id = os.path.basename(labels).split("_")[0]
                    db_connect.cur.execute(
                        "UPDATE hashtag_lib SET `status`=3 "
                        "WHERE sampleData_id={}".format(label_id)
                    )
                    print("Update `hashtag_lib`:\n\t", db_connect.cur.statement)
                except TimeoutError as e:
                    logging.error(str(e))

    if idx_cellranger.any():
        path = (
            args["tool_path"]
            if args["tool_path"]
            else os.path.join(os.path.expanduser("~"), "sera")
        )
        config_jobs_yml = os.path.join(path, "config", args["jobs"])
        jobs_yml_config(
            sample_data_[idx_cellranger],
            email=args["email"],
            config_jobs_yml=config_jobs_yml,
        )

        if CR:
            run(execp="sera_submit_mjobs.py", path=path, **args)

    if save:
        sample_data_.to_csv(args["results_output"])
    else:
        try:
            from tabulate import tabulate
        except ImportError:
            os.system("pip3 install tabulate")
            from tabulate import tabulate
        print(
            tabulate(
                sample_data_, headers="keys", tablefmt="fancy_grid", showindex=False
            )
        )

    db_connect.db.disconnect()

    return None
