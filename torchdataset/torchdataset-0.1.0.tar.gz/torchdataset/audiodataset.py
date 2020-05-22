import sys
import os
import os.path

import torch
import torch.utils.data as torchdata

from . import dataset


AUDIO_EXTENSIONS = (".wav", ".mp3")


def default_loader(path):
    # Sampling rate will be ignored
    waveform, sampling_rate = torchaudio.load(path)
    return waveform


class AudioFolder(dataset.DatasetFolder):
    """A generic data loader where the audio tracks are arranged in this way: ::

        root/car/xxx.wav
        root/car/xxy.wav
        root/car/xxz.wav

        root/home/123.wav
        root/home/nsdf3.wav
        root/home/asd932_.wav

    Args:
        root (string): Root directory path.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.
        is_valid_file (callable, optional): A function that takes path of an Image file
            and check if the file is a valid file (used to check of corrupt files)

     Attributes:
        classes (list): List of the class names sorted alphabetically.
        class_to_idx (dict): Dict with items (class_name, class_index).
        imgs (list): List of (image path, class_index) tuples
    """

    def __init__(self, root, transform=None, target_transform=None,
                 loader=default_loader, is_valid_file=None):
        super(AudioFolder, self).__init__(root, loader, AUDIO_EXTENSIONS if is_valid_file is None else None,
                                          transform=transform,
                                          target_transform=target_transform,
                                          is_valid_file=is_valid_file)
        self.tracks = self.samples
    

class PreLoadAudioFolder(dataset.AudioFolder):
     """A generic data loader storing all transformed data on memory,
        where the audio tracks are arranged in this way: ::

        root/car/xxx.wav
        root/car/xxy.wav
        root/car/xxz.wav

        root/home/123.wav
        root/home/nsdf3.wav
        root/home/asd932_.wav

    Args:
        root (string): Root directory path.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.
        is_valid_file (callable, optional): A function that takes path of an Image file
            and check if the file is a valid file (used to check of corrupt files)

     Attributes:
        classes (list): List of the class names sorted alphabetically.
        class_to_idx (dict): Dict with items (class_name, class_index).
        imgs (list): List of (image path, class_index) tuples
    """

   def __init__(self, *args, **kwargs):
        super(PreLoadAudioFolder, self).__init__(*args, **kwargs)
        self.load_all()
    
    def load_all(self):
        preprocessed_samples = []
        for i in range(len(self)):
            sys.stdout.write("\rloaded {0} / {1}".format(i+1, len(self)))
            sys.stdout.flush()
            path, target = self.samples[i]
            sample = self.loader(path)

            if self.transform is not None:
                sample = self.transform(sample)
            if self.target_transform is not None:
                target = self.target_transform(target)

            preprocessed_samples.append((sample, target))

        self.preprocessed_samples = preprocessed_samples
        sys.stdout.write("\n")

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        return self.preprocessed_samples[index]