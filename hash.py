#!/usr/bin/env python

import os
import sys
import argparse
import hashlib
import timeit
from tqdm import *
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

def hash(path):
	try:
                #print "Hashing " + path
		with open(path, 'rb') as f:
			hasher = hashlib.sha256()
                        for chunk in iter(lambda:f.read(8192), b''):
			    hasher.update(chunk)
		with open('hashes.txt', 'a') as w:
			w.write(hasher.hexdigest()+'\t'+path+'\n')
                #print "Hashed " + path
	except:
		if verbosity == 1:
			print "Couldn't hash file: " + path
		else:
			pass

def get_paths(path):
	paths = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			paths.append(os.path.join(root, name))
	return paths

def syshash(path):
        print "Reading filesystem..."

	paths = get_paths(path)	

        print "Found " + str(len(paths)) + " files"
        print "Hashing the files now..."
	
        t0 = timeit.default_timer()

        p = Pool(cpu_count()) 
        with tqdm(len(paths)) as pbar:
	    for i, _ in tqdm(enumerate(p.imap(hash, paths))):
                pbar.update()
	p.close()
	p.join()

        t1 = timeit.default_timer()
	
	print "Done! Hashed " + str(len(paths)) + " files in " + str(t1-t0) + "s"
        print "Hashes have been written to hashes.txt"

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
