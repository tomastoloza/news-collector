import news_collector
from inverted_index import consultar, create_index

if __name__ == '__main__':
    print('Bienvenido al recolector de noticias')

    while True:
        print('Seleccione: \n'
              '1. Recolectar noticias\n'
              '2. Crear indice invertido\n'
              '3. Comprimir lista de apariciones\n'
              '4. Realizar busquedas')
        user_input = input()
        if user_input == 1:
            NewsCollector().get_and_compare()
        if user_input == 2:
            pass
        if user_input == 3:
            pass
        if user_input == 4:
            consultar(create_index())
        if user_input == '':
            exit()
