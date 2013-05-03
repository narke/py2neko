#!/usr/bin/env python3

# Author: Konstantin Tcholokachvili
# Date: 2013

# This script is only for testing purposes, it's Unix dependent
# Note: You must be root to install it at /opt

import sys
import subprocess
import os
import shutil

TARGET_DIR = "/opt/py2neko/"

def is_nekovm_installed():
    status = subprocess.call(["which", "neko"])

    if status == 0:
        # the program is found and is executable
        return True
    else:
        return False


def copy_py2neko_files():
	py2neko_path = os.getcwd()
	
	if not os.path.isdir(TARGET_DIR):
		os.mkdir(TARGET_DIR)
		os.mkdir(TARGET_DIR + "/bin")
		os.mkdir(TARGET_DIR + "/lib")
	
	for (path, dirs, files) in os.walk(py2neko_path + "/modules"):
		for f in files:
			neko_module_file_path = os.path.join(path, f)
			# compile each neko module
			subprocess.call(["nekoc", neko_module_file_path])
			# and move to the target directory
			try:
				# once compiled: module.neko -> module.n
				os.rename(neko_module_file_path[:-3], os.path.join(TARGET_DIR + "/lib/", f[:-3]))
			except:
				print("Possibly this module wasn't compiled: %s" % neko_module_file_path[:-3])
				
	shutil.copy(py2neko_path + "/py2neko.py", TARGET_DIR + "/bin/py2neko.py")
	

if __name__ == '__main__':

    if sys.version_info < (3, 0):
        print("You need Python 3.0 or greater!")
        sys.exit()

    if not is_nekovm_installed():
        print("NekoVM isn't installed on your system! Install it first.")
    
    copy_py2neko_files()
    
    print("Installation done.")
