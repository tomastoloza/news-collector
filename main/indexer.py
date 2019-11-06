import csv
import os
import re
import string
import time

from lxml.etree import fromstring
from unidecode import unidecode

from nltk.stem import SnowballStemmer


class Indexer(object):

    def __init__(self):
        self.term_termID_dic = {}
        self.doc_docID_dic = {}
        self.indicator = 0
        self._STOP_WORDS = frozenset(['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los',
                                      'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'es',
                                      'lo', 'como',
                                      'más', 'pero', 'sus', 'le', 'ya', 'o', 'fue', 'este', 'ha', 'sí', 'porque',
                                      'esta', 'son',
                                      'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser', 'tiene', 'también',
                                      'me', 'hasta',
                                      'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos',
                                      'durante',
                                      'estados', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'fueron', 'ese', 'eso',
                                      'había',
                                      'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo',
                                      'otro', 'otras',
                                      'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos',
                                      'cual', 'sea',
                                      'poco', 'ella', 'estar', 'haber', 'estas', 'estaba', 'estamos', 'algunas', 'algo',
                                      'nosotros',
                                      'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros',
                                      'vosotras', 'os',
                                      'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo',
                                      'suya', 'suyos',
                                      'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra',
                                      'vuestros',
                                      'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis',
                                      'están',
                                      'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás',
                                      'estará',
                                      'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos',
                                      'estaríais',
                                      'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve',
                                      'estuviste',
                                      'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras',
                                      'estuviéramos',
                                      'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos',
                                      'estuvieseis',
                                      'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he',
                                      'has', 'ha',
                                      'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan',
                                      'habré', 'habrás',
                                      'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos',
                                      'habríais',
                                      'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube',
                                      'hubiste', 'hubo',
                                      'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos',
                                      'hubierais',
                                      'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen',
                                      'habiendo',
                                      'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois',
                                      'son', 'sea',
                                      'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos',
                                      'seréis', 'serán',
                                      'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos',
                                      'erais',
                                      'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras',
                                      'fuéramos',
                                      'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen',
                                      'siendo', 'sido',
                                      'sed', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga',
                                      'tengas',
                                      'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos',
                                      'tendréis',
                                      'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían',
                                      'tenía',
                                      'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo',
                                      'tuvimos',
                                      'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais',
                                      'tuvieran',
                                      'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo',
                                      'tenido', 'tenida',
                                      'tenidos', 'tenidas', 'tened', ''])
        self.stemmer = SnowballStemmer('spanish')

    def get_file_names(self):
        file_names = []
        files = [file for file in os.walk('../resources/rss/')]
        for num in range(1, len(files)):
            file_names.append((files[num][0], files[num][2]))
        return file_names

    def acondicionar_palabra(self, pal):
        """Should be used within a not None verifier"""
        if not re.compile(r'\w+=.+').match(pal) and not re.compile(r'<[^>]+>').match(pal) \
                and not re.compile(r'\d+').search(pal) and pal not in self._STOP_WORDS:
            pal = unidecode(pal)
            pal = pal.lower()
            pal = pal.strip(string.punctuation)
            pal = self.stemmer.stem(pal)
            if len(pal) > 3:
                return pal

    def BSBI_index_construction(self, data, name):
        """Siendo data una tupla con path del diario y una lista de las secciones """
        blocks = []
        n = 0
        for diario in data:
            try:
                block = self.parse_next_block(diario)
            except Exception as e:
                print(str(e))
            inverted_block = self.bsbi_invert(block)
            blockname = self.write_block_to_disk(inverted_block, n)
            blocks.append(blockname)
            n += 1
        self.merge_blocks(blocks, name)
        self.save_dictionaries()

    def parse_next_block(self, sections):
        """Iteracion por Secciones"""
        temp_not_inverted_dic = {}
        docID = len(self.doc_docID_dic)
        termID = len(self.term_termID_dic)
        for section in sections[1]:

            path = sections[0] + '/' + section
            print(path)
            with open(path, 'r', encoding="utf-8") as open_file:
                temp_not_inverted_dic.setdefault(docID, [])
                xml_parsed = fromstring(open_file.read())
                for item in xml_parsed:
                    try:
                        words = item.find('title').text + item.find('description').text
                        pub_date = item.find('pubDate').text
                    except IndexError:
                        words = item.find('title')
                        pub_date = 'sin fecha'
                    except TypeError:
                        pass
                    print(section)
                    medio = re.search('/(.+)/(.+)/(.+)', section).group(3)
                    section = re.search(r'(.+)\.xml', section).group(1)
                    section = medio + '-' + section + '-' + words + '-' + pub_date

                    if section not in self.doc_docID_dic.values():
                        self.doc_docID_dic[docID] = section
                    for word in words.split():
                        word = self.acondicionar_palabra(word)
                        if word is not None:
                            if word not in self.term_termID_dic.values():
                                self.term_termID_dic[termID] = word
                                temp_not_inverted_dic[docID].append(termID)
                                termID += 1
                            else:
                                for termIDinDIC in self.term_termID_dic:
                                    if self.term_termID_dic[termIDinDIC] == word and termIDinDIC not in \
                                            temp_not_inverted_dic[docID]:
                                        temp_not_inverted_dic[docID].append(termIDinDIC)
            docID = len(self.doc_docID_dic)
        return temp_not_inverted_dic

    def bsbi_invert(self, block):
        inverted_dic = {}
        for x in block:
            for y in block[x]:
                inverted_dic.setdefault(y, [])
                inverted_dic[y].append(x)
        return inverted_dic

    def write_block_to_disk(self, block, n):
        filename = str(n) + '.csv'
        with open(filename, 'w+', encoding='UTF-8', newline='') as open_file:
            writer = csv.writer(open_file)
            for x in sorted(block.keys()):
                fila_a_escribir = []
                fila_a_escribir.append(x)
                for b in block[x]:
                    fila_a_escribir.append(b)
                writer.writerow(fila_a_escribir)
        return filename

    def merge_blocks(self, blocks, name):
        inverted_dic = {}
        files = [open(file, 'r', encoding='UTF-8') for file in blocks]
        readers = [csv.reader(open_file) for open_file in files]
        line_processed_per_file = [1] * (len(blocks))
        next_line_to_process = [2] * (len(blocks))
        still_processing = True
        while still_processing:
            still_processing = False
            for reader in readers:
                for row in reader:
                    actual_index = readers.index(reader)
                    if line_processed_per_file[actual_index] <= reader.line_num < next_line_to_process[actual_index]:
                        inverted_dic.setdefault(int(row[0]), [])
                        for num in range(1, len(row)):
                            if int(row[num]) not in inverted_dic[int(row[0])]:
                                inverted_dic[int(row[0])].append(int(row[num]))
                        line_processed_per_file[actual_index] += 1
                        next_line_to_process[actual_index] += 1
                        still_processing = True
        self.write_block_to_disk(inverted_dic, name)
        [file.close() for file in files]

    def save_dictionaries(self):
        terms_id = 'terms_id.csv'
        docs_id = 'docs_id.csv'
        with open(terms_id, 'w+', encoding='UTF-8', newline='') as terms_id_file, open(docs_id, 'w+', encoding='UTF-8',
                                                                                       newline='') as docs_id_file:

            terms_writer = csv.writer(terms_id_file)
            docs_writer = csv.writer(docs_id_file)

            for x in sorted(self.term_termID_dic.keys()):
                row = []
                row.append(x)
                row.append(self.term_termID_dic[x])
                terms_writer.writerow(row)
            for x in sorted(self.doc_docID_dic.keys()):
                row = []
                row.append(x)
                row.append(self.doc_docID_dic[x])
                docs_writer.writerow(row)


if __name__ == '__main__':
    index = Indexer()
    index.BSBI_index_construction(index.get_file_names()[1:2], 'bsbi_1:2')
    index.save_dictionaries()
