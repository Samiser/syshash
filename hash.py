#!/usr/bin/env python3

import os
import sys
import argparse
import hashlib
import timeit
from tqdm import *
from subprocess import run, PIPE
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

def hash(path):
    try:
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda:f.read(8192), b''):
                hasher.update(chunk)
    except:
        if verbosity == 1:
            print("Couldn't hash file: %s" % path)
        else:
            pass
    else:
        return hasher.hexdigest(), path

def get_paths(path):
    paths = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            paths.append(os.path.join(root, name))
    return paths

def syshash(path):
    print("Reading filesystem...")
    paths = get_paths(path)

    print("Found %s files" % (str(len(paths))))
    print("Hashing the files now...")

    t0 = timeit.default_timer()

    p = Pool(cpu_count())
    with tqdm(len(paths)) as pbar:
        for digest, path in p.imap(hash, paths):
            with open('hashes.txt', 'a') as w:
                w.write("%s\t%s\n" % (digest, path))
            pbar.update()
    p.close()
    p.join()

    t1 = timeit.default_timer()
    SIZE = run("du -sb ~/Downloads/ -h | cut -f1", stdout=PIPE, shell=True).stdout.decode('utf-8')[:-2]
    print("Done! Hashed %s files (%sGB) in %ss" % (str(len(paths)), SIZE, str(t1-t0)))
    print("Hashes have been written to hashes.txt")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='Specify the folder to hash recursively')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    global verbosity
    verbosity = 0
    if args.verbose:
        verbosity = 1

    if args.directory:
        syshash(args.directory)
    else:
        syshash('/')
