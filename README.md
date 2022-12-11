# clean-human-eval-x
A cleaned version of the HumanEval-x dataset

## Usage

### Import dataset

To import a dataset, you can use the following command:

```sh
python data.py import --url <URL>
```

where `<URL>` is the URL of the dataset.

If you want to import from local tar.gz file, you can use the following command:

```sh
python data.py import --file <FILE>
```

where `<FILE>` is the path to the tar.gz file.

### Export dataset

To export a dataset, you can use the following command:

```sh
python data.py export --dir <DIR> --filename <NAME>
```

where `<DIR>` is the directory where the dataset is located and `<NAME>` is the name of the tar.gz file.

### Export to HuggingFace

To export a dataset to HuggingFace, you can use the following command:

```sh
python data.py hf --dir <DIR> --hfexport <NAME>
```

where `<DIR>` is the directory where the dataset is located and `<NAME>` is the directory where the files to be uploaded to HuggingFace are located.