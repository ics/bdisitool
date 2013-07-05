import csv
import argparse
import os
import ntpath
from disitool import disitool


def main(**args):
    with open(args['file']) as f:
        entries = csv.reader(f, delimiter=',', quotechar='"')
        out = []
        for row in entries:
            try:
                head, tail = ntpath.split(row[6])
                if tail not in out:
                    r = tail.split(os.extsep)
                    if r[1] in args['include']:
                        for dirname, dirnames, filenames in os.walk(args['path']):
                            for filename in filenames:
                                if filename == tail:
                                    fullpath = os.path.join(dirname, filename)
                                    print '[+]',  fullpath
                                    disitool.ExtractDigitalSignature(fullpath)

            except IndexError:
                pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bulk sigs check',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="file", default='autoruns.csv',
                        help='File to be parsed')
    parser.add_argument("-p", "--path", dest="path", default='.',
                        help='Search for files in this path')
    parser.add_argument("-c", "--check", dest="include", default=['dll', 'exe', 'sys'],
                        nargs='+', type=str,
                        help='Check only files with these extensions')
    args = parser.parse_args()

    main(**vars(args))