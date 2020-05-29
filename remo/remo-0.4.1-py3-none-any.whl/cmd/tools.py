import shutil


def is_tool_exists(tool):
    return bool(shutil.which(tool))
