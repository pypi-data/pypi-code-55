from pathlib import Path
import json
import logging
import os
import zipfile

from PIL import Image

import datasetinsights.constants as const
from datasetinsights.data.bbox import BBox2D
from datasetinsights.storage.gcs import GCSClient
from .base import Dataset


GROCERIES_GCS_PATH = "data/groceries"
GROCERIES_LOCAL_PATH = "groceries"
JSON_NAME = "annotations"
DATA_PREFIX_NAME = "groceries_real"
ANNOTATION_FILE_NAME = "annotation_definitions"
SPLITS = ("train", "val", "test")
VERSIONS = ("v2", "v3")

logger = logging.getLogger(__name__)


class GroceriesReal(Dataset):
    """Groceries Real dataset loader.

    Attributes:
        root (str): local directory where groceries_real dataset is saved
        groceries_real_data (list): training or testing data
        split (str): indicate split type of the dataset (train|val|test)
        transforms: callable transformation
        label_mappings (dict): a dict of {label_id: label_name} mapping
        version (str): version of GroceriesReal dataset, e.g. "v2", "v3".
        default version="v3".
    """

    def __init__(
        self,
        *,
        data_root=const.DEFAULT_DATA_ROOT,
        split="train",
        transforms=None,
        version="v3",
        **kwargs,
    ):
        """
        Args:
            data_root (str): root directory prdfix of all datasets
            split (str): indicate split type of the dataset (train|val|test)
            transforms: callable transformation
            version (str): version of GroceriesReal dataset
            groceries_data (list): a list of all image info in the json file
            data_indices (list): a list of indices for image info in the json
            file
            In annotations.json file, all the image info are saved in a list:
            [
                {
                "file_name": "IMG_4185.JPG",
                "annotations":[{
                    "label_id": 11,
                    "bboxs":[1692, 1386, 768, 133
                }]
                },
            ]
            In the txt files, it contains all the indices for image info in the
            json file:
            for example, in grocieres_real_train.txt, it looks like:
                0 1 2 3 4 5 6 7 8 9 10 11 12 13
                which represents indices of train data in annotations.json file
        """
        self.split = split
        if split not in SPLITS:
            raise ValueError(
                f"invalid value for split: {split}, possible values "
                f"are: {SPLITS}"
            )
        logger.info(f"split for groceries real is {split}")
        if version not in VERSIONS:
            raise ValueError(
                f"A valid dataset version should be set. "
                f"Available versons: {VERSIONS}"
            )
        self.root = os.path.join(data_root, GROCERIES_LOCAL_PATH)
        self.version = version
        self.download()
        self.groceries_data = self._get_annotations()
        self.data_indices = self._get_data_indices()
        self.transforms = transforms
        self.label_mappings = self._get_label_mappings()

    def __getitem__(self, idx):
        """
        Args:
            idx (int): index

        Returns:
            A tuple of image name and a list of bounding boxes inside the image
        """
        data_idx = self.data_indices[idx]
        image_data = self.groceries_data[data_idx]
        image_name = image_data["file_name"]
        annotations = image_data["annotations"]
        image = Image.open(
            os.path.join(self.root, self.version, "images", image_name)
        )
        bboxes = self._convert_annotations(annotations)
        if self.transforms:
            return self.transforms(image, bboxes)
        else:
            return (image, bboxes)

    def __len__(self):
        return len(self.data_indices)

    def _get_local_data_zip(self):
        """create a local path for download zip file
        """
        return os.path.join(self.root, f"{self.version}.zip")

    def _get_annotations(self):
        """Read data from the annotations.json.
        In the json file, image file name and annotations are saved in a list.
        For example:
            [
                {
                "file_name": "IMG_4185.JPG",
                "annotations":[{
                    "label_id": 11,
                    "bboxs":[1692, 1386, 768, 133
                }]
                },
            ]

        Return:
            json_data (list): a list of data in annotations.json file
        """
        json_data = json.load(
            open(os.path.join(self.root, self.version, f"{JSON_NAME}.json"))
        )

        return json_data

    def _convert_annotations(self, annotations):
        """Convert the bounding boxes for an image into canonical 2d bbox.

        Args:
            annotations (list): bounding box information from annotations.json

        Return:
            bboxes (list): a list of bounding box for an image
        """
        bboxes = []
        for ann in annotations:
            bbox = self._convert_canonical_2Dbbox(ann)
            bboxes.append(bbox)

        return bboxes

    def download(self):
        """download dataset from GCS
        """
        path = Path(self.root)
        path.mkdir(parents=True, exist_ok=True)
        client = GCSClient()
        data_zip_gcs = os.path.join(GROCERIES_GCS_PATH, f"{self.version}.zip")

        data_zip_local = self._get_local_data_zip()
        if not os.path.exists(data_zip_local):
            logger.info(f"no data zip file found, will download.")
            client.download(
                bucket_name=const.GCS_BUCKET,
                object_key=data_zip_gcs,
                localfile=data_zip_local,
            )

            with zipfile.ZipFile(data_zip_local, "r") as zip_dir:
                zip_dir.extractall(f"{self.root}")

    def _get_data_indices(self):
        """Get data indices from txt file.

        Returns:
            idx_data (list): a list of data indices in self.groceries_data
        """
        file_path = os.path.join(
            self.root, self.version, f"{DATA_PREFIX_NAME}_{self.split}.txt"
        )
        with open(file_path) as txt_file:
            idx_data = [int(i) for i in txt_file.readline().split()]

        return idx_data

    def _get_label_mappings(self):
        """Get data indices from txt file.

        Returns:
            label_mappings (dict): a dict of {label_id: label_name} mapping
        """
        file_path = os.path.join(
            self.root, self.version, f"{ANNOTATION_FILE_NAME}.json"
        )
        with open(file_path) as json_file:
            init_definition = json.load(json_file)["annotation_definitions"][0]
            label_mappings = {
                m["label_id"]: m["label_name"] for m in init_definition["spec"]
            }

        return label_mappings

    def _convert_canonical_2Dbbox(self, single_bbox):
        """Convert BBobx to canonical BBox2D.

        Args:
            single_bbox (dict): raw bounding box information

        Return:
            canonical_bbox (BBox2D): canonical bounding box
        """
        label = single_bbox["label_id"]
        bbox = single_bbox["bbox"]

        canonical_bbox = BBox2D(
            x=bbox[0], y=bbox[1], w=bbox[2], h=bbox[3], label=label
        )
        return canonical_bbox
