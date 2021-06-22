import os
from os.path import Path
import glob
import jsonlines


class DataTransform:
    """
    Transforms data from the JSONL structure to the required structure
    for the FLAIR code.
    """

    def __init__(self, data_path: str, out_dir: str, recurse_dirs: bool = True):
        """
        Initializes the object.

        :param {str} data_path - The path to the JSONL data directory.
        :param {str} out_dir - The output directory
        :param {bool} recurse_dirs - Whether to recurse directories or not.
        """
        self.data_path = data_path
        self.out_dir = out_dir
        self.recurse_dirs = recurse_dirs

    def transform(self):
        path = Path(self.data_path)
        out_path = Path(self.out_dir)

        if self.recurse_dirs:
            file_list = path.rglob('*.jsonl')
        else:
            file_list = path.glob('*.jsonl')

        for file in file_list:
            with jsonlines.open(file) as reader:
                to_write = list(reader.iter(type=str, skip_invalid=True))

                with open(out_path / file.name, 'w') as f:
                    f.write('\n'.join(to_write))
