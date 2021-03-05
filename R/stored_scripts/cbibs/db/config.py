# -*- coding: utf-8 -*-
import logging
from configparser import ConfigParser
import os

'''
Utility to read the configuration file. File contents should look like:
[postgresql]
host=140.90.200.61
database=ncbo
user=cbibs_dbo
password=<<password>>

'''


def config(filename='database.ini', section='postgresql'):
    # create a parser, read file and throw an exception if you can't read it
    parser = ConfigParser()
    configFile = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(configFile):
        logging.error("Can't find configuration file")
        raise Exception('Filename {0} not found'.format(configFile))
    # read config file
    parser.read(configFile)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
