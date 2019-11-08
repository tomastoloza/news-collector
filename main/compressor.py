import array
import csv
import sys


class Compressor:
    def encode(self, postings_list):
        return array.array('L', postings_list).tobytes()

    def decode(self, encoded_postings_list):
        decoded_postings_list = array.array('L')
        decoded_postings_list.frombytes(encoded_postings_list)
        return decoded_postings_list.tolist()

    def comprimir_indice(self, inverted_index):
        big_byte_string = b''
        byte_inverted_index = {}
        with open(inverted_index, 'r', encoding='UTF-8') as open_file:
            reader = csv.reader(open_file)
            for row in reader:
                int_row = []
                for value in row:
                    int_row.append(int(value))
                term = int_row[:1]
                docs = int_row[1:]
                byte_inverted_index.setdefault(term[0], ())
                start_position = len(big_byte_string)
                quantity_of_docs = len(docs)
                size_of_docs = sys.getsizeof(self.encode([docs[0]]))
                byte_inverted_index[term[0]] = (start_position, quantity_of_docs, size_of_docs)
                for doc in docs:
                    big_byte_string += self.encode([doc])
        with open('compressed_inverted_index.csv', 'w+', encoding='UTF-8', newline='') as open_file:
            writer = csv.writer(open_file)
            for x in byte_inverted_index.keys():
                fila_a_escribir = []
                fila_a_escribir.append(x)
                for value in byte_inverted_index[x]:
                    fila_a_escribir.append(value)
                writer.writerow(fila_a_escribir)
        with open('byte_string.txt', 'wb+') as open_file:
            open_file.write(big_byte_string)

    def comprimir_indice_con_saltos(self, inverted_index):
        big_byte_string = b''
        byte_inverted_index = {}
        with open(inverted_index, 'r', encoding='UTF-8') as open_file:
            reader = csv.reader(open_file)
            for row in reader:
                int_row = []
                for value in row:
                    int_row.append(int(value))
                term = int_row[:1]
                docs = int_row[1:]
                byte_inverted_index.setdefault(term[0], ())
                start_position = len(big_byte_string)
                quantity_of_docs = len(docs)
                size_of_docs = sys.getsizeof(self.encode([docs[0]]))
                byte_inverted_index[term[0]] = (start_position, quantity_of_docs, size_of_docs)
                first_doc = docs[0]
                big_byte_string += self.encode([first_doc])
                previous_doc = first_doc
                for doc in docs:
                    jump = doc - previous_doc
                    previous_doc = doc
                    if jump == 0:
                        pass
                    else:
                        big_byte_string += self.encode([jump])
        with open('compressed_inverted_index_with_jumps.csv', 'w+', encoding='UTF-8', newline='') as open_file:
            writer = csv.writer(open_file)
            for x in byte_inverted_index.keys():
                fila_a_escribir = []
                fila_a_escribir.append(x)
                for value in byte_inverted_index[x]:
                    fila_a_escribir.append(value)
                writer.writerow(fila_a_escribir)
        with open('byte_string_with_jumps.txt', 'wb+') as open_file:
            open_file.write(big_byte_string)

    def search_termID_appearances_in_compressed_dic(self, term_id):
        start_position = 0
        final_position = 0
        termID_docs = []
        with open('compressed_inverted_index.csv', 'r', encoding='UTF-8') as inverted_dic_file:
            reader = csv.reader(inverted_dic_file)
            for row in reader:
                if int(row[0]) == term_id:
                    start_position = int(row[1])
                    final_position = start_position + int(row[2]) * 4 + 1
        with open('byte_string.txt', 'rb+') as byte_string_file:
            list_to_decode = []
            cant_y = 0
            for x in byte_string_file:
                for y in x:
                    cant_y += 1
                    if start_position < cant_y < final_position:
                        list_to_decode.append(y)
                        if len(list_to_decode) == 4:
                            final_summatory = list_to_decode[0] * 256 ** 0 + list_to_decode[1] * 256 ** 1 + \
                                              list_to_decode[2] * 256 ** 2 + list_to_decode[3] * 256 ** 3
                            termID_docs.append(final_summatory)
                            list_to_decode = []
        return termID_docs

    def search_termID_appearances_in_compressed_dic_with_jumps(self, term_id):
        start_position = 0
        final_position = 0
        termID_docs = []
        with open('compressed_inverted_index_with_jumps.csv', 'r', encoding='UTF-8') as inverted_dic_file:
            reader = csv.reader(inverted_dic_file)
            for row in reader:
                if int(row[0]) == term_id:
                    start_position = int(row[1])
                    final_position = start_position + int(row[2]) * 4 + 1
        with open('byte_string_with_jumps.txt', 'rb+') as byte_string_file:
            list_to_decode = []
            cant_y = 0
            for x in byte_string_file:
                for y in x:
                    cant_y += 1
                    if start_position < cant_y < final_position:
                        list_to_decode.append(y)
                        if len(list_to_decode) == 4:
                            final_summatory = list_to_decode[0] * 256 ** 0 + list_to_decode[1] * 256 ** 1 + \
                                              list_to_decode[2] * 256 ** 2 + list_to_decode[3] * 256 ** 3
                            termID_docs.append(final_summatory)
                            list_to_decode = []
        final_result = []
        final_result.append(termID_docs[0])
        previous = termID_docs[0]
        for value in termID_docs[1:]:
            summatory = previous + value
            final_result.append(summatory)
            previous = summatory
        return final_result

