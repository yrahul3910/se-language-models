# SE Language Models

The goal of this repository is to provide a set of pre-trained language models fine-tuned for the SE domain. We
will use state-of-the-art models, train them, and release the trained models online.


## Getting Started

There are two ways to get a pre-trained model: you can train the models yourself, or use our pre-trained model (250k steps with a batch size of 8).

### Download a pre-trained model

If using a pre-trained model, you can ignore the steps below. However, if you want to further train these models, you will need to follow the steps below. Our pre-trained models are stored on S3. The easiest way to access the pre-trained models is through the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Once you have the CLI tool installed, you can directly copy the models from the bucket to your local file system. You will need 11.4GB free space for all 6 models.

```
aws s3 cp s3://se-language-models ./ --recursive
```

### Download the data

Please download the datasets from [archive.org](https://archive.org/download/stackexchange), who host the Stack Exchange data dumps. You may download as many as needed for your application. The torrent method is faster for downloading; we recommend [qBitTorrent](https://www.qbittorrent.org/download.php).

### Extract the data

We extract the data using a simple one-line shell script. Install `p7zip` for your system, using the package manager (`brew` for macOS, `apt` for Debian-based systems, `dnf` for Fedora/RHEL-based systems or the Windows Subsystem for Linux on Windows). Then, run:

```sh
for file in *.7z; do mkdir $(basename $file .7z); 7z x $file -o$(basename $file .7z); done
```

This extracts each 7z file to a directory with the same name, sans the extension.

### Preprocessing

Preprocessing is done using [@sotorrent's pipeline](https://github.com/sotorrent/preprocessing-pipeline/). Please use that to convert the raw data to JSONL files for each Stack Exchange forum. In our implementation, the pipeline writes to a Google Cloud Storage bucket. The files can be copied using:

```sh
until gsutil -m cp -L log.txt -r CLOUD_BUCKET_PATH .; do sleep 1; done 
```

**JSONL to text file**

Next, run `jsonl-to-text.py`, which converts the JSONL data to text files. You may need to update the paths in this file before running it.

```
python3 jsonl-to-text.py
```

**Text files to train/valid/test split**

Finally, `reorganize.py` will create a train, validation, and test file.

```
python3 reorganize.py LOCATION_OF_TEXT_FILES OUTPUT_DIR
```

## Training

You can train the models using `train_lm_hf.py` and `train_w2v.py`, depending on whether you want to train a language model or word2vec. While `train_w2v.py` will work without running `reorganize.py`, `train_lm_hf.py` requires that structure. 

`train_w2v.py` takes in the directory of the text files as a command-line argument.

```
python3 train_w2v.py TEXT_FILES_DIR
```

Update `train_lm_hf.py` to set the path and model parameters at line 13-17, and training args at line 78-85.
