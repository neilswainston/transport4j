'''
(c) University of Liverpool 2019

All rights reserved.

@author: neilswainston
'''
# pylint: disable=invalid-name
import os
import shutil
import sys

from transport4j import tcdb


def _makedirs(dir_name):
    '''Make directory, deleting existing one if present.'''
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    os.makedirs(dir_name)


def main(args):
    '''main method.'''

    # Generate neo4j import file directories:
    out_dir = args[1]
    nodes_dir = os.path.join(out_dir, 'nodes')
    rels_dir = os.path.join(out_dir, 'rels')
    _makedirs(nodes_dir)
    _makedirs(rels_dir)

    # Parse tcdb data:
    df = tcdb.parse(args[0])
    df.to_csv(os.path.join(nodes_dir, 'tcdb.csv'), index=False)


if __name__ == '__main__':
    main(sys.argv[1:])
