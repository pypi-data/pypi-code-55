from pytconf.config import ParamCreator, Config


class ConfigRepository(Config):
    """
    Parameters to specify the repository
    """
    folder = ParamCreator.create_existing_folder(
        default="/mnt/seagate/mark/topics_archive/audio/abooks/by_name",
        help_string="where is the repository",
    )


class ConfigNames(Config):
    """
    Parameters for names authorization repository
    """
    repository = ParamCreator.create_existing_file(
        help_string="file where authorized strings are located",
        default="/home/mark/.mp3lib_authorized_non_ascii.json",
    )
    repository_backup = ParamCreator.create_existing_file(
        help_string="file where authorized strings are located",
        default="/home/mark/.mp3lib_authorized_non_ascii.json.back",
    )
    all_over = ParamCreator.create_bool(
        default=False,
        help_string="start from scratch",
    )


class Authorized(Config):
    """
    stuff which is authorized
    """
    chars_ok_for_folders = ParamCreator.create_str(
        help_string="Which chars are allowed for folders",
        default=""
    )
    chars_ok_for_files = ParamCreator.create_str(
        help_string="Which chars are allowed for files",
        default="“”ìú"
    )
