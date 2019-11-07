import functools
from main.inverted_index import acondicionar_palabra


class Searcher(object):

    def search(self, words, inverted_index_file):
        result = []
        for word in words.split():
            with open('docs_id_dict.csv', 'r') as file:
                for line in file.readlines():
                    if word in line:
                        print(word)

            # try:
            #     docs = functools.reduce(lambda x, y: x + ", " + y,
            #                             [doc for doc in inverted_index_file[acondicionar_palabra(word)]])
            #     result.append((word, docs))
            # except KeyError:
            #     result.append((word, {}))
            # except TypeError:
            #     pass
        return result


if __name__ == '__main__':
    s = Searcher()
    b = s.search('ndea')
    print(b)
