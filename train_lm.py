from flair.embeddings import TransformerWordEmbeddings
from flair.data import Dictionary
from flair.trainers.language_model_trainer import LanguageModelTrainer, TextCorpus


model = TransformerWordEmbeddings('bert-base-uncased'
                                  fine_tune=True).lm
is_forward_lm = model.is_forward_lm
dictionary = Dictionary.load('chars')
corpus = TextCorpus('../data/processed/',
                    dictionary,
                    is_forward_lm)

trainer = LanguageModelTrainer(model, corpus)
trainer.train('./models/', mini_batch_size=2)

"""
# Alternatively:

trainer = ModelTrainer(model, corpus)
trainer.fine_tune('../models/', mini_batch_size=2)
"""
