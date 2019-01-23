# !/usr/bin/python

import hashlib
import os

def hashDir(path):
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			with open(root+"/"+name, 'rb') as file:
				hasher = hashlib.sha256()
				hasher.update(file.read());
				print hasher.hexdigest() + "\t" + name	

if __name__ == "__main__":
	hashDir("/")	
