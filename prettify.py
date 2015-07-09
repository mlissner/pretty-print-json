#!/usr/bin/python
import fnmatch
import json
import os

from sys import stdout

__author__ = 'mlissner'

import argparse


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError(
            "readable_dir:{0} is not a readable dir".format(prospective_dir))


def make_pretty(dir):
    """"Recurse through a directory, opening every JSON file, and then making it
    pretty.
    """

    print "Recursively walking the directory to find all files..."
    matches = []
    count = 0
    for root, dirnames, filenames in os.walk(dir):
        for filename in fnmatch.filter(filenames, '*.json'):
            matches.append(os.path.join(root, filename))
            count += 1
            stdout.write("\rFound:\t\t%s" % count)
            stdout.flush()

    print "\nProcessing the files..."

    completed = 0
    for match in matches:
        with open(match, 'r') as j_file:
            j = json.load(j_file)
        with open(match, 'w') as j_out:
            json.dump(j, j_out, indent=2)
        completed += 1
        stdout.write("\rComplete:\t\t%s" % completed)
        stdout.flush()

    print "\nDone!"


def main():
    parser = argparse.ArgumentParser(
        description='Make a bunch of ugly JSON files into pretty JSON files!'
    )
    parser.add_argument(
        '-d',
        '--directory',
        type=readable_dir,
        default='.',
        help='The directory you wish to prettify.'
    )

    args = parser.parse_args()

    make_pretty(args.directory)

if __name__ == '__main__':
    main()
