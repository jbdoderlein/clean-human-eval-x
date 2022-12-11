"""
Script to download the data from the web and save it locally, 
and exporting the data as a tar.gz file.
"""

import os
import requests
import argparse
import gzip
import shutil
import tarfile

def download_data(url, filename):
    """
    Download data from the web and save it locally
    """
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
            
def unpack_data(filename, new_filename):
    """
    Unpack the data
    """
    with tarfile.open(filename, 'r:gz') as f_in:
        f_in.extractall(new_filename)
        

def export_data(filename: str, new_filename: str) -> None:
    """
    Export the data as a tar.gz file
    """
    with tarfile.open(new_filename, "w:gz") as tar:
        tar.add(filename, arcname=os.path.basename(filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['import', 'export'])
    parser.add_argument("--url", type=str)
    parser.add_argument("--filename", type=str, default="data.gz")
    parser.add_argument("--dir", type=str, default="data")
    args = parser.parse_args()
    if args.mode == 'import':
        # If url then download first
        if args.url:
            filename = download_data(args.url, args.filename)
        unpack_data(args.filename, "")
    elif args.mode == 'export':
        export_data(args.dir, args.filename)
    else:
        print("Unknown mode")
        exit(1)