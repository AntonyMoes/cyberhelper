from model import get_model
from ast import literal_eval
import numpy as np


class Generator:
    def __init__(self, file: str = 'trained_data/cyber_weights'):
        with open('trained_data/char_indices') as f:
            char_indices = f.read()
        self._char_indices = literal_eval(char_indices)

        with open('trained_data/indices_char') as f:
            indices_char = f.read()
        self._indices_char = literal_eval(indices_char)

        self._chars = sorted(list(self._char_indices.keys()))

        self._maxlen = 40

        self._model = get_model(self._maxlen, len(self._chars))
        self._model.load_weights(file)

    def generate(self, seed: str = '', size: int = 50, diversity: float = 0.25):
        generated = ''
        sentence = 'хорошего дня хорошего дня хорошего дня  '

        if seed != '':
            seed_chars = set(seed)
            for char in seed_chars:
                if char not in self._chars:
                    pos = seed.find(char)
                    while pos != -1:
                        if pos == len(seed) - 1:
                            seed = seed[:pos]
                        else:
                            seed = seed[:pos] + seed[pos+1]
                        pos = seed.find(char)

            if len(seed) > self._maxlen:
                seed = seed[:self._maxlen]
            sentence = seed + sentence[len(seed):]
        generated += sentence
        print(f'Sentence: {sentence}')

        i = 0
        next_char = ' '
        while i < size or (next_char != ' ' and next_char != '\n'):
            x_pred = np.zeros((1, self._maxlen, len(self._chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, self._char_indices[char]] = 1.

            preds = self._model.predict(x_pred, verbose=0)[0]
            next_index = self._sample(preds, diversity)
            next_char = self._indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
            i += 1
            print(i)

        return generated[40:-1] + '.'

    @staticmethod
    def _sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)


if __name__ == '__main__':
    generator = Generator()
    text = generator.generate()
    print(text)
