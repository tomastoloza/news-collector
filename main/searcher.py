import functools
from main.indexer import Indexer


class Searcher(object):

    def search(self, words):
        result = {}
        term_ids = {}
        for word in words.split():
            word = Indexer().acondicionar_palabra(word)
            with open('../resources/dictionaries/terms_id.csv', 'r') as file:
                for line in file.readlines():
                    if word == line.split(',')[1].strip('\n'):
                        term_ids.setdefault(line.split(',')[0], list())
                        term_ids[line.split(',')[0]].append(word)

        for term in term_ids:
            result.setdefault(term_ids[term][0], list())
            with open('../resources/dictionaries/bsbi.csv', 'r') as file:
                line = file.read().split('\n')[int(term)]
                line = line.strip('\n')
                term_ids[term].append(line.split(',')[1:])

        for term in term_ids:
            with open('../resources/dictionaries/docs_id.csv', 'r') as file:
                word = term_ids[term][0]
                for line in file.readlines():
                    for doc in term_ids[term][1]:
                        if doc == line.split(',')[0].strip('\n'):
                            result[word].append(functools.reduce(lambda x, y: x + y, line.split(',')[1:]))
        return result


if __name__ == '__main__':
    b=Searcher().search('macri fernandez')
    print(b)