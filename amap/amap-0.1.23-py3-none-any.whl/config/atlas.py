from neuro.atlas import Atlas

transpositions = {
    "horizontal": (1, 0, 2),
    "coronal": (2, 0, 1),
    "sagittal": (2, 1, 0),
}


class AtlasError(Exception):
    pass


class RegistrationAtlas(Atlas):
    """
    A class to handle all the atlas data (including the
    """

    def __init__(self, config_path, dest_folder=""):
        super().__init__(config_path)
        self.dest_folder = dest_folder

        self._pix_sizes = None  # cached to avoid reloading atlas

        if self["orientation"] != "horizontal":
            raise NotImplementedError(
                "Unknown orientation {}. Only horizontal supported so far".format(
                    self.original_orientation
                )
            )

    def get_dest_path(self, atlas_element_name):
        if not self.dest_folder:
            raise AtlasError(
                "Could not get destination path. "
                "Missing destination folder information"
            )
        return str(self.dest_folder / self[atlas_element_name])
