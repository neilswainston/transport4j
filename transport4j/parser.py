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
    tcdb_df = tcdb.parse(args[0])

    # Extract relationships:
    trns_org_df = tcdb_df.loc[:, ['id', 'organism']]
    trns_org_df[':TYPE'] = 'HAS_ORGANISM'
    trns_org_df.dropna(inplace=True)
    trns_org_df.rename(columns={'id': ':START_ID',
                                'organism': ':END_ID'},
                       inplace=True)

    # Reformat tcdb data:
    tcdb_df[':LABEL'] = 'Protein|Transporter'
    tcdb_df.drop('organism', axis=1, inplace=True)
    tcdb_df.drop_duplicates(subset='id', inplace=True)
    tcdb_df.rename(columns={'id': 'id:ID'}, inplace=True)

    # Generate organism data:
    org_df = trns_org_df[':END_ID'].drop_duplicates().to_frame()
    org_df[':LABEL'] = 'Organism'
    org_df.rename(columns={':END_ID': 'name:ID'}, inplace=True)

    # Write input files:
    tcdb_df.to_csv(os.path.join(nodes_dir, 'trns.csv'), index=False)
    org_df.to_csv(os.path.join(nodes_dir, 'org.csv'), index=False)
    trns_org_df.to_csv(os.path.join(rels_dir, 'trns_org.csv'), index=False)


if __name__ == '__main__':
    main(sys.argv[1:])
