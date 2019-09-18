'''
(c) GeneGenie Bioinformatics Ltd. 2018

All rights reserved.

@author: neilswainston
'''
import os
import shutil


def makedirs(dir_name):
    '''Make directory, deleting existing one if present.'''
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    os.makedirs(dir_name)
