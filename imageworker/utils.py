import yaml
from pathlib import Path
from shutil import copyfile

"""
Get config from yml file
"""


def getConfig():
    parameters_file = Path("config/parameters.yml")
    if parameters_file.is_file() is False:
        copyfile('imageworker/config/parameters.yml.dist', 'imageworker/config/parameters.yml')

    stream = open("imageworker/config/parameters.yml", "r")
    config = yaml.load_all(stream)
    data = {}
    for parameters in config:
        for key, value in parameters.items():
            data[key] = value

    return data
