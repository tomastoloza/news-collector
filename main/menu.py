import functools

from main.indexer import Indexer
from main.inverted_index import consultar
from main.news_collector import NewsCollector
from main.searcher import Searcher


class Menu(object):
    def __init__(self):
        self.searcher = Searcher()
        self.indexer = Indexer()
        # self.compressor = Compressor()

    def run_menu(self):
        print('Bienvenido al recolector de noticias')
        while True:
            menu = 'Seleccione: \n1. Recolectar noticias\n2. Crear indice invertido\n3. Comprimir lista de apariciones\n4. Realizar busquedas\n'
            user_input = input(menu)
            if user_input == '1':
                rss = NewsCollector().iterate_rss()
                print('\nLos siguientes diarios fallaron:\n')
                for item in rss:
                    print('Diario: {} Sección: {} URL: {}\n'.format(item[0][0], item[0][1], item[1]))
            if user_input == '2':
                print('Construyendo indice invertido en disco')
                self.indexer.BSBI_index_construction(self.indexer.get_file_names())
                print('Finalizado. Ver resultados en /resources/dictionaries')
            # if user_input == '3':
                # self.compressor.comprimir_indice()
            if user_input == '4':
                self.search()
                continue
            if user_input == '':
                exit()

    def search(self):
        while True:
            user_input = input("\nIntroduce tu búsqueda (Enter para finalizar):\n>>> ")
            if len(user_input) == 0:
                break
            results = self.searcher.search(user_input)
            for re in results:
                print('Resultados de ' + re + ':')
                for item in results[re]:
                    print(item, '\n')


if __name__ == '__main__':
    menu = Menu()
    menu.run_menu()
