import os
import pydicom
from pathlib import Path
from pydicom.tag import Tag
from collections import namedtuple
from pathlib import Path
import logging
from datetime import datetime


Filter = namedtuple('Filter', ['id', 'description', 'value', 'long_desc'])

now = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

root = Path(os.path.abspath(__file__)).parent
logpath = root / 'logs'
ANON_LOG_FILE = logpath / f"{now}.log"


if not os.path.exists(logpath):
    os.makedirs(logpath)

logging.basicConfig(filename=ANON_LOG_FILE,
                    filemode='a',
                    format='%(asctime)s %(levelname)s \t %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def generate_tags(user_list):
    tags = []
    for line in user_list:
        line = Filter(*line)
        tag = Tag([int(x, 16) for x in line.id.split(",")])  # Convert hex to int and get Tag
        tags.append(Filter(tag, line.description, line.value, line.long_desc))
    return tags


def load_dicom_file(filepath):
    try:
        return pydicom.dcmread(os.path.join(filepath))
    except pydicom.errors.InvalidDicomError:
        logging.error("Invalid DICOM")
        return None


def save_dicom_file(ds, savepath):
    savepath.parent.mkdir(parents=True, exist_ok=True)
    ds.save_as(str(savepath))
    print(f"Saving: {savepath}\n")
    logging.info(f"Saving: {savepath}\n\n")


def scrub_tags(ds, tags):
    for tag in tags:
        try:
            value_cur = ds[tag.id].value
            value_new = tag.value

            logging.info(f"{tag.id} {tag.description}: \t Found (replacing {value_cur} with {value_new})")
            ds[tag.id].value = value_new
        except KeyError:
            logging.error(f"{tag.id} {tag.description}: \t Not found (KeyError)")
        except AttributeError:
            logging.error(f"{tag.id} {tag.description}: \t Not found (AttributeError)")
        except TypeError:
            logging.error(f"{tag.id} {tag.description}: \t Not found (TypeError)")
        except:
            logging.error(f"{tag.id} {tag.description}: \t Unexpected error")

    return ds


def anonymise_file(source_filepath, dest_filepath, tags):
    f = Path(source_filepath)
    ds = load_dicom_file(source_filepath)

    if ds:
        print(f"Opening: {f}")
        logging.info(f"Opening: {f}")
        ds_anon = scrub_tags(ds, tags)

        # TODO handle better
        # savefile = os.path.join(f.parent, f"{f.stem}_anon.dcm")
        save_dicom_file(ds_anon, dest_filepath)
