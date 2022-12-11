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
from pathlib import Path
import json

EXTENSION = {
    'python': '.py',
    'cpp': '.cpp',
    'java': '.java',
    'js': '.js',
    'go': '.go'
}

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
    parser.add_argument('mode', choices=['import', 'export', 'hf'])
    parser.add_argument("--url", type=str, help="URL to import from. If not provided, filename is used.")
    parser.add_argument("--filename", type=str, default="humaneval_x_clean.gz", help="Filename to import from")
    parser.add_argument("--dir", type=str, default="humaneval", help="Directory to export from.")
    parser.add_argument("--hfexport", type=str, default="hfexport", help="Directory to export to for Hugging Face.")
    args = parser.parse_args()
    if args.mode == 'import':
        # If url then download first
        if args.url:
            filename = download_data(args.url, args.filename)
        unpack_data(args.filename, "")
    elif args.mode == 'export':
        export_data(args.dir, args.filename)
    elif args.mode == 'hf':
        # create a dir of dir name
        Path(args.hfexport).mkdir(parents=True, exist_ok=True)
        # Copy humaneval-x-clean.py to the dir
        shutil.copyfile("humaneval-x-clean.py", os.path.join(args.hfexport, "humaneval-x-clean.py"))
        # for each language in the dir
        for lang in os.listdir(args.dir):
            # create a dir of lang name
            Path(os.path.join(args.hfexport, lang)).mkdir(parents=True, exist_ok=True)
            # create a jsonl file
            with open(os.path.join(args.hfexport, lang, "humaneval.jsonl"), "w") as ex_f:
                for problem in os.listdir(os.path.join(args.dir, lang, "prompt")):
                    data = {}
                    data['task_id'] = f"{lang}/{problem.replace(EXTENSION[lang], '')}"
                    with open(os.path.join(args.dir, lang, "prompt", problem)) as f:
                        data['prompt'] = f.read()
                    with open(os.path.join(args.dir, lang, "test", problem)) as f: 
                        data['test'] = f.read()
                    with open(os.path.join(args.dir, lang, "solution", problem)) as f: 
                        data['canonical_solution'] = f.read()
                    ex_f.write(json.dumps(data))
                    ex_f.write("\n")
    else:
        print("Unknown mode")
        exit(1)