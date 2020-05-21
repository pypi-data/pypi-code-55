import os
import re
import sys
import json
import click
import shutil

config = dict()

def replace_values(text, config=config):
    """
    Replace template with values.
    INPUT:
        text (str): String to find and replace keys from the config dict.
        config (dict): Dictionary to map every key to be replaced by it's value.
    OUTPUT:
        replaced_text (str): Text with keys replaced by values.
        num_occur (int): Number of keys replaced.
    """
    try:
        num_occur = 0

        # for every key in config
        for key in config:
            # replace keys in text by it's value
            template = "{{romeo." + key + "}}"
            text, n = re.subn(template, config[key], text)
            num_occur += n

        return text, num_occur
    except:
        raise
        return text, 0


def copy_files(src, dst):
    """
    Copy source file to destination while renaming and replacing the content if it finds a template value.
    INPUT:
        src (str): Path for the source file.
        dst (str): Path for the destination directory.
    OUTPUT:
        None
    """
    new_dst, _ = replace_values(dst)
    shutil.copy2(src, new_dst)

    with open(new_dst, mode="r+") as f:
        new_content, n = replace_values(f.read())
        
        # just delete the content and saves the new if the file was changed.
        if n > 0:
            f.truncate(0)
            f.write(new_content)


def rollback():
    """
    Rollback the project creation by removing the entire folder
    """
    try:
        shutil.rmtree(config['name'])
    except:
        raise


@click.command()
@click.option('--name', prompt='Project Name', help='Name used to create new project.')
@click.option('--description', prompt='Project Description', help='A short description about the project.')
@click.option('--author_name', prompt="Author's Name", help='Name of the author.')
@click.option('--author_email', prompt="Author's Email", help='Email to contact the author.')
def init(name, description, author_name, author_email): 
    """
    Generates a new Romeo project.
    The template project follows the Cookiecutter Data Science.
    """
    config['name'] = name
    config['description'] = description
    config['author_name'] = author_name
    config['author_email'] = author_email

    try:
        # get source directory
        source = os.path.join(os.path.dirname(__file__), '..', 'template')
        
        # check if template folder exists
        if os.path.exists(source):
            # copy template folder to name and replace files templates
            shutil.copytree(source, name, copy_function=copy_files)

            # generate romeo.json
            with open(os.path.join(name, 'romeo.json'), mode="w+") as config_file:
                json.dump(config, config_file, indent=4)
        else:
            print("Failed to locate template folder")
    except FileExistsError:
        rollback()
        print("Folder already exists")
    except:
        rollback()
        raise

if __name__ == "__main__":
    sys.exit(init())
