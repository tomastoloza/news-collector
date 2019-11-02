import os
import string
import csv
from xml.etree.ElementTree import fromstring


def get_doc_id():
    pass


def get_term_id(word):
    return word.hash()


def get_file_names():
    file_names = []
    files = [file for file in os.walk('../resources/rss/')]
    for num in range(1, len(files)):
        for file in files[num][2]:
            file_names.append(files[num][0] + '/' + file)
    return file_names


_STOP_WORDS = frozenset(['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los',
                         'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'es', 'lo', 'como',
                         'más', 'pero', 'sus', 'le', 'ya', 'o', 'fue', 'este', 'ha', 'sí', 'porque', 'esta', 'son',
                         'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser', 'tiene', 'también', 'me', 'hasta',
                         'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos', 'durante',
                         'estados', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'fueron', 'ese', 'eso', 'había',
                         'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras',
                         'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'sea',
                         'poco', 'ella', 'estar', 'haber', 'estas', 'estaba', 'estamos', 'algunas', 'algo', 'nosotros',
                         'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os',
                         'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos',
                         'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros',
                         'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están',
                         'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará',
                         'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais',
                         'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste',
                         'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos',
                         'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis',
                         'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha',
                         'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás',
                         'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais',
                         'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo',
                         'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais',
                         'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo',
                         'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea',
                         'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán',
                         'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais',
                         'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos',
                         'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'siendo', 'sido',
                         'sed', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas',
                         'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis',
                         'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía',
                         'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos',
                         'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran',
                         'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida',
                         'tenidos', 'tenidas', 'tened', ''])


def acondicionar_palabra(pal):
    replace = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    pal = pal.lower()
    pal = pal.strip()
    pal = pal.strip(string.punctuation + "»" + "\x97" + "¿" + "¡" + "”" + "“" + "'&quot" + 'br/>' + "\"")
    for a, b in replace:
        pal = pal.replace(a, b)
    return pal


def create_index():
    import re
    term_id_dict = {}
    doc_id_dict = {}
    inverted_id_dict = {}
    counter_term_id = 0
    counter_doc_id = 0
    for file_name in get_file_names():
        file = open(file_name, 'r', encoding="utf-8").read()
        file_text = fromstring(file)
        for item in file_text:
            title = item[0]
            pub_date = 'sin fecha'
            try:
                sandwich = item[1].text + ' ' + item[0].text
                pub_date = item[1].text
            except IndexError:
                sandwich = item[0].text
            except TypeError:
                pass

            regex = re.search('\/(.+)\/(.+)\/(.+)', file_name)
            if title.text != None:
                strip = title.text
                strip = strip.strip()
                strip = strip.replace('\n', ' ')
                doc_id_dict.setdefault(counter_doc_id, '')
                doc_id_dict[counter_doc_id] = regex.group(2) + '-' + regex.group(3)[:-4] + '-' + strip + '-' + pub_date

            for word in sandwich.split():
                word = acondicionar_palabra(word)
                # TODO: metodo
                if word.count('href=') == 0 and word.count('src=') == 0 and word.count('alt=') == 0 and not bool(
                        re.search(r'\d', word)) and word not in _STOP_WORDS and len(word) > 3:
                    if word not in term_id_dict.values():
                        term_id_dict.setdefault(counter_term_id, '')
                        term_id_dict[counter_term_id] = word
                        inverted_id_dict.setdefault(counter_doc_id, set())
                        inverted_id_dict[counter_doc_id].add(counter_term_id)
                        counter_term_id += 1
                    else:
                        word_id = 0
                        for x in term_id_dict:
                            if term_id_dict[x] == word:
                                word_id = x
                        inverted_id_dict.setdefault(counter_doc_id, set())
                        inverted_id_dict[counter_doc_id].add(word_id)
            counter_doc_id += 1
    with open("term_id_dict.csv", "w+", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for x in term_id_dict:
            list = [str(x), term_id_dict[x]]
            writer.writerow(list)
    with open("doc_id_dict.csv", "w+", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for x in doc_id_dict:
            list = [str(x), doc_id_dict[x]]
            writer.writerow(list)
    with open("inverted_index.csv", "w+", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for x in inverted_id_dict:
            list = [str(x), inverted_id_dict[x]]
            writer.writerow(list)

    return inverted_id_dict


if __name__ == '__main__':
    b = create_index()
    print(b)
