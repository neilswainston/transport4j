'''
(c) University of Liverpool 2019

All rights reserved.

@author: neilswainston
'''
# pylint: disable=invalid-name
import os.path
import re
import sys
import urllib

from Bio import SeqIO

import pandas as pd


def parse(out_dir='data'):
    '''Get data.'''

    # Parse fasta data:
    fasta_df = _get_fasta_df(out_dir)
    # fasta_df.to_csv('fasta.csv', index=False)

    # Parse human data:
    human_df = pd.concat(
        [pd.read_csv(_get_file('human.csv', out_dir)),
         pd.read_csv(_get_file('human_specific.csv', out_dir))])

    human_df = human_df.drop_duplicates()
    human_df['organism'] = 'Homo sapiens'
    human_df.rename(columns={'Accession': 'uniprot'}, inplace=True)
    # human_df.to_csv('human.csv', index=False)

    # Consolidate:
    return pd.concat([fasta_df, human_df], sort=False)


def _get_fasta_df(out_dir):
    '''Get fasta DataFrame.'''
    regex = re.compile(
        r'gnl\|TC-DB\|([^\|]+)\|(\S+) ?([^\[]*) ?(?:(?:\[)(.*)(?:\]))?')

    data = []

    for record in SeqIO.parse(_get_file('tcdb', out_dir), 'fasta'):
        match = regex.match(record.description)

        data.append([term.strip() if term else term
                     for term in match.groups()] + [record.seq])

    df = pd.DataFrame(data,
                      columns=['id', 'TCID', 'Name', 'organism', 'Sequence'])

    df = df.apply(_parse_name, axis=1)

    return df


def _parse_name(row):
    '''Parse Name field from fasta.'''
    # Parse Name field:
    regex = re.compile(r'\s+([A-Z]{2})=')
    terms = regex.split(row['Name'])

    # Generate dict:
    pairs = dict(_grouped(terms[1:], 2))

    if pairs:
        # If source is inferred as uniprot, update ids accordingly:
        pairs['uniprot'] = row.get('id', None)
        row.drop('id')

    pairs['Name'] = terms[0]
    pairs['organism'] = row['organism'] if row['organism'] \
        else pairs.get('OS', None)
    pairs.pop('OS', None)

    # Update row:
    for key, value in pairs.items():
        row[key] = value

    return row


def _grouped(iterable, n):
    '''Group list into chunks of length n.'''
    return zip(*[iter(iterable)] * n)


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
    df = parse(args[0])
    df.to_csv('out.csv', index=False)


if __name__ == '__main__':
    main(sys.argv[1:])
