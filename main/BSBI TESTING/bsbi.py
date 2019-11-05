import csv

documents = ["Bombadil.txt", "Egidio.txt", "Niggle.txt", "Roverandom.txt", "Wootton.txt"]

term_termID_dic = {}
doc_docID_dic = {}
indicator = 0


def BSBI_index_construction(data):
    blocks = []
    n = 0
    while True:
        n += 1
        block = parse_next_block(size, position)
        bsbi_invert(block)
        blockname = write_block_to_disk(block, n)
        blocks.append(blockname)
        if (n == 10):
            break
    merge_blocks(blocks)


def parse_next_block(size, position=(0, 0, 0)):
    position_actual = list(position[:])
    temp_not_inverted_dic = {}
    docID = position_actual[0] + 1
    termID = len(term_termID_dic) + 1
    tempSize = 0
    for doc in documents[position_actual[0]:]:
        print(position_actual)
        print("DOC ID: " + str(docID))
        line_number = position_actual[1]
        with open(doc, 'r', encoding='UTF-8') as open_file:
            print(doc)
            actual_line = 0
            temp_not_inverted_dic.setdefault(docID, [])
            if doc not in doc_docID_dic.values():
                doc_docID_dic[docID] = doc
            for line in open_file:
                if actual_line == position_actual[1]:
                    list_per_line = line.split(" ")
                    line_number += 1
                    for word in list_per_line:
                        if "\\" in r"%r" % word or len(word) <= 3:
                            pass
                        else:
                            if word not in term_termID_dic.values():
                                term_termID_dic[termID] = word
                                temp_not_inverted_dic[docID].append(termID)
                                termID += 1
                                tempSize += 1
                            else:
                                for termIDinDIC in term_termID_dic:
                                    if term_termID_dic[termIDinDIC] == word and termIDinDIC not in \
                                            temp_not_inverted_dic[docID]:
                                        temp_not_inverted_dic[docID].append(termIDinDIC)
                                        tempSize += 1
                        if tempSize >= size:
                            break
                else:
                    actual_line += 1
                if tempSize >= size:
                    break
            if tempSize >= size:
                break
        position_actual[0] += 1
        position_actual[1] = 0
        position_actual[2] = 0
        docID += 1
        print("La position actual despues de procesar el texto es: " + str(position_actual[0]) + ", " + str(
            position_actual[1]) + ", " + str(position_actual[2]))
        if tempSize >= size:
            break
    print("TermID = " + str(termID))
    print(temp_not_inverted_dic)
    last_key = 0
    for keys in temp_not_inverted_dic:
        last_key = keys
    position = (position_actual[0], line_number - 1,
                term_termID_dic[temp_not_inverted_dic[last_key][(len(temp_not_inverted_dic[last_key])) - 1]])
    return temp_not_inverted_dic, position


def bsbi_invert(block):
    inverted_dic = {}
    for x in block:
        for y in block[x]:
            inverted_dic.setdefault(y, [])
            inverted_dic[y].append(x)
    return inverted_dic


def write_block_to_disk(block, n):
    with open(str(n) + '.csv', 'w+', encoding='UTF-8', newline='') as open_file:
        writer = csv.writer(open_file)
        for x in sorted(block.keys()):
            fila_a_escribir = []
            fila_a_escribir.append(x)
            fila_a_escribir.append(block[x])
            writer.writerow(fila_a_escribir)


def get_size_of_blocks(data):
    wordlist = []
    for x in data:
        print("TEXTO = " + x)
        with open(x, 'r', encoding='UTF-8') as file:
            for line in file:
                list_per_line = line.split(" ")
                for x in list_per_line:
                    if "\\" in r"%r" % x:
                        pass
                    else:
                        wordlist.append(x)
    print("the size is " + str(len(wordlist)))
    get_first_divisors(len(wordlist))


def get_first_divisors(number):
    list_of_divisors = []
    for i in range(1, 20):
        if number % i == 0:
            print("good!, " + str(i) + " has worked as a divisor")
            list_of_divisors.append(i)
        else:
            print('This division is no good, the result is: ' + str(number % i))
    print('this is the list of the first 20 divisors:\n')
    for x in list_of_divisors:
        print('if you divide the file in ' + str(x) + ' blocks, the size of each one will be: ' + str(number / x))


def merge_blocks(blocks):
    pass


if __name__ == '__main__':
    n = 0
    asd = parse_next_block(5000)
    while asd[1][0] <= len(documents):
        parcial_block = bsbi_invert(asd[0])
        write_block_to_disk(parcial_block, n)
        n += 1
        asd = parse_next_block(5000, asd[1])
