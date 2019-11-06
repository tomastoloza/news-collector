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
        with open('new_inverted.csv', 'w+', encoding='UTF-8') as open_file:
            writer = csv.writer(open_file)
            for x in byte_inverted_index.keys():
                fila_a_escribir = []
                fila_a_escribir.append(x)
                for value in byte_inverted_index[x]:
                    fila_a_escribir.append(value)
                writer.writerow(fila_a_escribir)
        with open('byte-string.txt', 'wb+') as open_file:
            open_file.write(big_byte_string)


if __name__ == '__main__':
    with open('byte-string.txt', 'rb+') as open_file:
        a = open_file.read()
        print(Compressor().decode(a))
