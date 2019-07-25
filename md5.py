import hashlib
import os, os.path
import sys
import re
import shutil
import time

files = os.listdir('./')
for file in files:
    if re.match('.*gz$', file):
        with open(os.path.join('./', file), 'rb') as f:
            checksum = hashlib.md5(f.read()).hexdigest()
            print(f"{checksum}  {file}")