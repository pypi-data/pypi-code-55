import pytest
from pathlib import Path
import numpy as np

from dvdp.utils.data import DataSaver


def test_create_and_load_chunks(tmpdir):
    data_saver = DataSaver(
        Path(tmpdir) / 'test',
        ['col1', 'col2'],
        chunk_size=4,
    )
    expected = {'col1': [], 'col2': []}
    for i in range(8):
        new = {'col1': i+1, 'col2': i}
        data_saver.add_data(new)
        expected['col1'].append(new['col1'])
        expected['col2'].append(new['col2'])

    result = DataSaver.load_data(Path(tmpdir) / 'test_000.gz')
    assert result == expected


def test_with_image(tmpdir):
    data_saver = DataSaver(
        Path(tmpdir) / 'test',
        ['col1', 'col2'],
        chunk_size=4,
    )
    expected = {'col1': [], 'col2': []}
    for i in range(8):
        image = np.full((4, 4), i)
        new = {'col1': image, 'col2': image}
        data_saver.add_data(new)
        expected['col1'].append(new['col1'])
        expected['col2'].append(new['col2'])

    result = DataSaver.load_data(Path(tmpdir) / 'test_000.gz')
    assert len(result) == len(expected)
    for images_rs, images_exp in zip(result.values(), expected.values()):
        assert len(images_rs) == len(images_exp)
        for image_rs, image_exp in zip(images_rs, images_exp):
            assert np.all(image_rs == image_exp)

