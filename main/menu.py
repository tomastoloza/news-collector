import functools

from main.inverted_index import consultar
from main.news_collector import NewsCollector
from main.searcher import Searcher


class Menu(object):
    def __init__(self):
        self.searcher = Searcher()

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
                menu = 'Seleccione:\n1. Crear un índice invertido a partir de la estructura de directorio y archivos xml\n2. Guardar en disco todo el índice invertido.\n3. Cargar en memoria un índice invertido previamente salvado.\n'
                user_input = input(menu)
                if user_input == '1':
                    pass
                if user_input == '2':
                    pass
                if user_input == '3':
                    pass
                if user_input == '4':
                    pass
                if user_input == '':
                    exit()
            if user_input == '3':
                pass
            if user_input == '4':
                self.search()
            if user_input == '':
                exit()

    def search(self):
        while True:
            user_input = input("\nIntroduce tu búsqueda (Enter para finalizar):\n>>> ")
            if len(user_input) == 0:
                break
            results = self.searcher.search(user_input)
            if len(results) > 0:
                for result in results:
                    print('La palabra ' + result + ' apareció en los documentos:\n' + functools.reduce(
                        lambda x, y: x  + y, results[result]))
            else:
                print('La palabra ' + user_input + ' no tuvo apariciones')


if __name__ == '__main__':
    menu = Menu()
    menu.run_menu()
