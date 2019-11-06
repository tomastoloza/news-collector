import functools
from main.inverted_index import acondicionar_palabra


class Searcher(object):

    def search(self, words, inverted_index_file):
        result = []
        for word in words.split():
            try:
                docs = functools.reduce(lambda x, y: x + ", " + y,
                                        [doc for doc in inverted_index_file[acondicionar_palabra(word)]])
                result.append((word, docs))
            except KeyError:
                result.append((word, {}))
            except TypeError:
                pass
        return result
