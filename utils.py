import yaml
from pathlib import Path
from shutil import copyfile

"""
Get config from yml file
"""


def getConfig():
    parameters_file = Path("apiclient/parameters.yml")
    if parameters_file.is_file() is False:
        copyfile('parameters.yml.dist', 'parameters.yml')

    stream = open("parameters.yml", "r")
    config = yaml.load_all(stream)
    data = {}
    for parameters in config:
        for key, value in parameters.items():
            data[key] = value

    return data
