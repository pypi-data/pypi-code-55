import os
import click
import json
import logging
import rich
import rich.table
import rich.console
import rich.logging
from multiprocessing import Process, Manager, Pool
import tqdm
import requests

import spb
from spb.cli_core.utils import recursive_glob_image_files
from spb.models.label import Label

console = rich.console.Console()

NUM_MULTI_PROCESS = 4
LABEL_DESCRIBE_PAGE_SIZE = 10


class LabelData():
    def upload_data_and_label(self, project_config, dataset_name, log_file, is_force):
        spb.client()
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        project_id = project_config[1]

        imgs_path = recursive_glob_image_files(dataset_name)
        if not click.confirm(f"Upload {len(imgs_path)} files to project '{project_config[0]}'. Proceed?"):
            return
        asset_images = []
        for key in imgs_path:
            file_name = key
            asset_image = {
                'file': imgs_path[key],
                'file_name': file_name,
                'data_key': key,
                'dataset': dataset_name
            }
            asset_images.append(asset_image)

        with Pool(NUM_MULTI_PROCESS) as p:
            list(tqdm.tqdm(p.imap(_upload_asset, zip([project_id] * len(asset_images), asset_images)), total=len(asset_images), desc="Uploading Data"))

        with Pool(NUM_MULTI_PROCESS) as p:
            labels = list(p.imap(_describe_label_by_asset, zip([project_id] * len(asset_images), asset_images)))

        if sum(label['result'] is not None for label in labels) > 0:
            if not is_force and not click.confirm(f"{sum(label['result'] is not None for label in labels)} files are already labeled. Overwrite?"):
                return

        with Pool(NUM_MULTI_PROCESS) as p:
            list(tqdm.tqdm(p.imap(_update_label, zip([project_id] * len(labels), labels)), total=len(labels), desc="Uploading labels"))


    def download_data_and_label(self, project_config, log_file):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

        project_id = project_config[1]
        command = spb.Command(type='describe_project')
        projects = spb.run(command=command, option={"id":project_id})
        label_count = projects[0].label_count
        page_length = int(label_count/LABEL_DESCRIBE_PAGE_SIZE) if label_count % LABEL_DESCRIBE_PAGE_SIZE == 0 else int(label_count/LABEL_DESCRIBE_PAGE_SIZE)+1

        logging.info("Calculating the total number of labels")
        with Pool(NUM_MULTI_PROCESS) as p:
            labels_list = list(p.imap(_describe_label_by_page, zip([project_id] * page_length, range(page_length))))
            labels = [item for sublist in labels_list for item in sublist]

        if not click.confirm(f"Download {len(labels)} files from project '{project_config[0]}'. Proceed?"):
            return

        with Pool(NUM_MULTI_PROCESS) as p:
            for _ in tqdm.tqdm(p.imap(_download_label_data, labels), total=len(labels)):
                pass

def _describe_label_by_page(args):
    logging.debug(f'_describe_label_by_page: {args}')

    [project_id, page_idx] = args
    command = spb.Command(type='describe_label')
    labels = spb.run(command=command, option={
        'project_id' : project_id
    }, page_size = LABEL_DESCRIBE_PAGE_SIZE, page = page_idx + 1)
    return labels

def _download_label_data(label):
    data_url = label.data_url
    path = label.dataset + label.data_key if label.data_key.find('/') != -1 else label.dataset + "/"+label.data_key
    os.makedirs(os.path.dirname(path), exist_ok=True)
    label_json_path = f'{path}.json'
    path = f'{path}'
    r = requests.get(data_url, allow_redirects=True)
    open(path, 'wb').write(r.content)
    open(label_json_path, 'w').write(label.toJson())

def _upload_asset(args):
    logging.debug(f'Uploading Asset: {args}')

    [project_id, asset_image] = args
    try:
        command = spb.Command(type='create_data')
        spb.run(command=command, option=asset_image, optional={'projectId': project_id})

    except Exception:
        logging.info(f'Failed to Upload Asset: {args}')
        pass

def _describe_label_by_asset(args):
    [project_id, asset_image] = args

    data_key = asset_image['data_key']
    dataset = asset_image['dataset']
    command = spb.Command(type='describe_label')
    option = {
        "project_id": project_id,
        "data_key": data_key,
        "dataset": dataset
    }

    labels = spb.run(command=command, option=option, page_size=1, page=1)
    label = labels[0]

    return {
        "id": label.id,
        "project_id": label.project_id,
        "data_key": label.data_key,
        "dataset": label.dataset,
        "result": label.result,
    }

def _update_label(args):
    [project_id, label] = args

    data_key = label['data_key']
    dataset = label['dataset']

    json_path = f"{dataset}/{data_key}.json"

    if not os.path.isfile(json_path):
        return

    try:
        with open(json_path) as json_file:
            json_data = json.load(json_file)

        if json_data['result'] == None:
            return
        label['result'] = json_data['result']

        command = spb.Command(type='update_label')
        label = spb.run(command=command, option=label)

        with open(json_path, 'w') as f:
           f.write(label.toJson())

    except Exception as err:
        console.print(err)
        console.print(f"Error while updating label '{label['data_key']}.json'. Try again.")
        logging.info(f"Error while updating label {args}")
