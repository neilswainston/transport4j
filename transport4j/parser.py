'''
(c) University of Liverpool 2019

All rights reserved.

@author: neilswainston
'''
import os
import sys

from transport4j import tcdb, writer


def main(args):
    '''main method.'''
    df = tcdb.parse(args[0])

    # Generate neo4j import files:
    out_dir = args[1]
    nodes_dir = os.path.join(out_dir, 'nodes')
    rels_dir = os.path.join(out_dir, 'rels')
    writer.makedirs(nodes_dir)
    writer.makedirs(rels_dir)


if __name__ == '__main__':
    main(sys.argv[1:])
