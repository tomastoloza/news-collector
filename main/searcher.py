import functools
from main.bsbi import acondicionar_palabra


class Searcher(object):

    def search(self, words, inverted_index):
        result = []
        for word in words.split():
            try:
                docs = functools.reduce(lambda x, y: x + ", " + y,
                                        [doc for doc in inverted_index[acondicionar_palabra(word)]])
                result.append((word, docs))
            except KeyError:
                result.append((word, {}))
            except TypeError:
                pass
        return result
