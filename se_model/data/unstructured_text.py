from datasets import load_dataset
from transformers import AutoTokenizer
from typing import List, Callable
from pathlib import Path
from se_model.utils import error
import os


class UnstructuredTextDataset:
    """
    A class that abstracts away the details of loading a text dataset.
    """

    def __init__(self, corpus_path: str) -> None:
        """
        Initializes the object. The path must be to a corpus/ folder with the
        following structure:

        corpus/
        corpus/train/
        corpus/train/XX.txt
        corpus/valid.txt
        corpus/test.txt

        :param {str} corpus_path - The path to the corpus folder. 
        """
        self.corpus_path = Path(corpus_path)

        # Assert that the path exists
        if not os.path.exists(corpus_path):
            error("Path to corpus does not exist.")
            return

        self.dataset = load_dataset('text', data_files={
            'train': os.listdir(self.corpus_path/'train'),
            'test': self.corpus_path/'test.txt'
        })

    def get_prepared_data(self, for_model: str, preprocess_fns: List[Callable] = None):
        """
        Preprocess the data and return it.

        :param {str} for_model - The model that this will be used for.
        :param {list} preprocess_fn - An optional list of callables that preprocess the
        dataset. Passed a single param of type datasets.Dataset. Refer to their
        docs (https://huggingface.co/docs/datasets/processing.html) for more help. These
        functions should NOT tokenize the data; that is done already.
        """
        tokenizer = AutoTokenizer.from_pretrained(for_model)

        def _tokenize_func(examples):
            return tokenizer(examples, padding='max_length', truncation=True)

        # Now run the user-specified preprocessing steps
        if preprocess_fns is not None:
            for fn in preprocess_fns:
                self.dataset = fn(self.dataset)

        # Tokenize
        tokenized_data = self.dataset.map(_tokenize_func, batched=True)

        return tokenized_data
