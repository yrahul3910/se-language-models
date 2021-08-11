from gensim.models.word2vec import PathLineSentences
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec
import sys


class LossLogger(CallbackAny2Vec):
    '''Output loss at each epoch'''

    def __init__(self):
        self.epoch = 1
        self.losses = []

    def on_epoch_begin(self, model):
        print(f'Epoch: {self.epoch}', end='\t', flush=True)

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        self.losses.append(loss)
        print(f'  Loss: {loss}')
        self.epoch += 1


if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} PATH_TO_CORPUS')
    sys.exit(1)

path = sys.argv[1]
files = PathLineSentences(path)
model = Word2Vec(files, workers=8, epochs=5,
                 compute_loss=True, callbacks=[LossLogger()])
model.save('word2vec.w2v')
