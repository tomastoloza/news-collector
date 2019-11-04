from main.bsbi import create_index
from main.inverted_index import consultar
from main.news_collector import NewsCollector

if __name__ == '__main__':
    print('Bienvenido al recolector de noticias')

    while True:
        menu = 'Seleccione: \n1. Recolectar noticias\n2. Crear indice invertido\n3. Comprimir lista de apariciones\n4. Realizar busquedas\n'
        user_input = input(menu)
        if user_input == '1':
            NewsCollector().iterate_rss()
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
            consultar(create_index())
        if user_input == '':
            exit()
