from flair.data import Dictionary
from flair.trainers.language_model_trainer import LanguageModelTrainer, TextCorpus
from flair.embeddings import TransformerDocumentEmbeddings


class Trainer:
    def __init__(self, path: str, model: str = 'bert-base-uncased'):
        """
        Initializes the trainer.

        :param {str} path - The path to the corpus folder
        :param {str} model - The model to train
        """
        dictionary = Dictionary.load('chars')
        self.corpus = TextCorpus(
            path, dictionary, forward=True, character_level=True)

        self.model = TransformerDocumentEmbeddings(model)
        self.trainer = LanguageModelTrainer(self.model, self.corpus)

    def train(self, save_dir: str = 'saved_models/', epochs: int = 10):
        """
        Trains the model.

        :param {int} epochs - Number of epochs to train
        :param {str} save_dir - Where to save the trained models
        """
        self.trainer.train('saved_models', max_epochs=epochs, checkpoint=True)
