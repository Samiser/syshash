# !/usr/bin/python

import os
import sys
import argparse
import hashlib
from multiprocessing.dummy import Pool

def hash(path):
	try:
		with open(path, 'rb') as f:
			hasher = hashlib.sha256()
			hasher.update(f.read())
		with open('hashes.txt', 'a') as w:
			w.write(hasher.hexdigest()+'\t'+path+'\n')
	except:
		if verbosity == 1:
			print "Couldn't hash file: " + path + "\n It was probably a broken symlink"
		else:
			pass

def get_paths(path):
	paths = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			paths.append(os.path.join(root, name))
	return paths

def syshash(path):
	paths = get_paths(path)	
	
	pool = Pool()
	pool.map(hash, paths)
	pool.close()
	pool.join()
	
	print "Done! Hashed " + str(len(paths)) + " files."

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
