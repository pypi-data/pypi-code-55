# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage_bucket']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'google-cloud-storage>=1.28.1,<2.0.0',
 'returns>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'storage-bucket',
    'version': '0.4.0',
    'description': 'Easy to work with Google Cloud Platform Storage Bucket wrapper',
    'long_description': "[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n# Google Cloud Platform Storage Bucket\n\nThis package just aims to make life a little bit easier for people who have to work with google cloud storage bucket.\n\n\n## Quickstart:\n\n1. get the package\n  * `pip install storage-bucket`\n2. Download your keyfile and save it as key.json and point to it with env var:\n  * `gcloud iam service-accounts keys create key.json --iam-account your_service_account@your_project.iam.gserviceaccount.com`\n  * `export GOOGLE_APPLICATION_CREDENTIALS='key.json'`\n3. Run some code:\n\n\n```python\nfrom storage_bucket.download_file import DownloadFile, download_file\n\n\ndef use_data_for_something(data):\n    print(data)\n\n\n# Normal way, this might throw exception...\nmy_data = download_file(\n    'my_bucket',\n    'my_file.txt',\n)\nuse_data_for_something(my_data)\n\n\n# Returns Modal way\n# this will _only_ call use_data_for_something when data is successfully downloaded.\nDownloadFile()(\n    'my_bucket',\n    'my_file.txt',\n).map(\n    use_data_for_something,  # send data to this function,\n).alt(\n    print,  # print error or send a mail or w/e\n)\n```\n\n## Supported functions\n\n### Downloading\n\n```python\nfrom storage_bucket.download_file import DownloadFile, download_file\n\nDownloadFile()('bucket', 'filename')\ndownload_file('bucket', 'filename')\n```\n\n### Uploading\n```python\nfrom storage_bucket.upload_file import UploadFile, upload_file\n\nUploadFile()(b'data', 'bucket_name', 'filename')\nupload_file(b'data', 'bucket_name', 'filename')\n```\n\n### Listing\n```python\nfrom storage_bucket.list_files import ListFiles, list_files\n\nListFiles()('bucket')\nlist_files('bucket')\n\nListFiles()('bucket', 'foldername/')\nlist_files('bucket', 'foldername/')\n```\n\n### Deleting\n```python\nfrom storage_bucket.delete_file import DeleteFile, delete_file\n\nDeleteFile()('bucketname', 'filename')\ndelete_file('bucketname', 'filename')\n```\n\n### List Buckets\n```python\nfrom storage_bucket.list import ListBuckets, list_buckets, list_bucket_names\n\nbuckets = ListBuckets()()\nbucket_names = list_bucket_names(buckets.unwrap())\n\nbuckets2 = list_buckets()\nbucket_names2 = list_bucket_names(buckets2)\n```\n\n\n\n### The use of [Returns](https://github.com/dry-python/returns) library.\n  * Just lets us get rid of all exceptions.\n  * Lets us chain stuff so everything looks good.\n  * Lets you use `DownloadFile()(args...).map(dostuff).alt(dostuffonfailure)`\n  * Don't like it? use the matching normal function provided for your convenience.\n",
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasborgen/storage-bucket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
