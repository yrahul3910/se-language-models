# SE Language Models

The goal of this repository is to provide a set of pre-trained language models fine-tuned for the SE domain. We
will use state-of-the-art models, train them, and release the trained models online.


## Getting Started

### Download the data

Please download the datasets from [archive.org](https://archive.org/download/stackexchange), who host the Stack Exchange data dumps. You may download as many as needed for your application. The torrent method is faster for downloading; we recommend [qBitTorrent](https://www.qbittorrent.org/download.php).

### Extract the data

We extract the data using a simple one-line shell script. Install `p7zip` for your system, using the package manager (`brew` for macOS, `apt` for Debian-based systems, `dnf` for Fedora/RHEL-based systems or the Windows Subsystem for Linux on Windows). Then, run:

```
for file in *.7z; do mkdir $(basename $file .7z); 7z x $file -o$(basename $file .7z); done
```

This extracts each 7z file to a directory with the same name, sans the extension.

### Preprocessing

Preprocessing is done using [@sotorrent's pipeline](https://github.com/sotorrent/preprocessing-pipeline/). Please use that to convert the raw data to JSONL files for each Stack Exchange forum. In our implementation, the pipeline writes to a Google Cloud Storage bucket. The files can be copied using:

```sh
until gsutil -m cp -L log.txt -r CLOUD_BUCKET_PATH .; do sleep 1; done 
```


## Tests

Some parts of this code have tests written to check that they work correctly. These have been placed *beside the code* to keep each part of the code together. As it stands, the tests are not written as unit tests, but as self-contained modules that can be run on sample inputs.

