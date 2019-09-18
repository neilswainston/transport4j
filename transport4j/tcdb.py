'''
(c) University of Liverpool 2019

All rights reserved.

@author: neilswainston
'''
import os.path
import re
import sys
import urllib

from Bio import SeqIO

import pandas as pd


def parse(out_dir='data'):
    '''Get data.'''
    fasta_df = _get_fasta_df(out_dir)
    fasta_df.to_csv('fasta.csv', index=False)

    human_df = pd.concat(
        [pd.read_csv(_get_file('human.csv', out_dir)),
         pd.read_csv(_get_file('human_specific.csv', out_dir))])

    human_df = human_df.drop_duplicates()
    human_df.to_csv('human.csv', index=False)

    return None


def _get_fasta_df(out_dir):
    '''Get fasta DataFrame.'''
    regex = re.compile(
        r'gnl\|TC-DB\|([^\|]+)\|(\S+) ?([^\[]*) ?(?:(?:\[)(.*)(?:\]))?')

    data = []

    for record in SeqIO.parse(_get_file('tcdb', out_dir), 'fasta'):
        match = regex.match(record.description)

        data.append(list(match.groups()) + [record.seq])

    return pd.DataFrame(data,
                        columns=['id', 'tcdb_id', 'name', 'organism', 'seq'])


def _get_file(filename, out_dir):
    '''Get file.'''
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    path = os.path.join(out_dir, filename)

    if not os.path.exists(path):
        url_dir = 'http://www.tcdb.org/public/'
        urllib.request.urlretrieve('%s%s' % (url_dir, filename), path)

    return path


def main(args):
    '''main method.'''
    parse(args[0])


if __name__ == '__main__':
    main(sys.argv[1:])
