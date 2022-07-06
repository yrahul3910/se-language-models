import re
from pathlib import Path
import jsonlines
from se_model.utils import unmark, error


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

    def _replace(self, line, pre, post):
        """
        Replace all occurrences of a pattern pre with post
        in a line.

        :param {str} line - The line to work with
        :param {str} pre - The regex to match
        :param {str} post - The regex to replace with
        :return {str} The processed line.
        """
        return re.sub(pre, post, line)

    def _process_line(self, line: list):
        """Process a single line."""
        if not isinstance(line, list):
            error('Param line must be of type list.')
            raise ValueError('Incorrect param type.')

        try:
            line = unmark('\n'.join(line))  # Parse md
        except:
            line = '\n'.join(line)
            print('Unmark failed, skipping.')
            print(line)

        # The long regex is for URLs, from https://www.urlregex.com/
        return self._replace(
            self._replace(
                self._replace(
                    self._replace(
                        line, '@\S+', ''  # Remove mentions
                    ), '<img.*?/>', ''  # Remove images
                ), '</?kbd>', ''  # Remove <kbd> tags, keep content
            ), 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ''
        )

    def transform(self):
        path = Path(self.data_path)
        out_path = Path(self.out_dir)

        if self.recurse_dirs:
            file_list = path.rglob('*.jsonl')
        else:
            file_list = path.glob('*.jsonl')

        file_list = list(file_list)
        for i, file in enumerate(file_list):
            print(f'[{i+1} / {len(file_list)}] Processing {file}')
            # Ignore non-UTF-8 characters
            with open(file, 'r', errors='ignore') as f:
                reader = jsonlines.Reader(f)

                processed_lines = []
                for line in reader.iter(type=list):
                    processed_lines.append(
                        self._process_line(line[-1]['text_blocks']))
                    processed_lines.append(
                        self._process_line(line[-1]['comments']))

                write_path = out_path / (file.name + '.processed')
                write_path.touch()

                with open(write_path, 'w') as f:
                    f.write('\n'.join(processed_lines))
