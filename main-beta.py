import pandas as pd

NOTAS_ALUMNOS_PATH = r'inputs/Notas_Alumnos.xlsx'
print(NOTAS_ALUMNOS_PATH)

dict_asig = {
    'LENGUA CASTELLANA Y LITERATURA':   'Lengua Castellana y Literatura',
    'BIOLOGIA':                         'Biología',
    'GEOGRAFIA E HISTORIA':             'Geografía e Historia',
    'MATEMATICAS':                      'Matemáticas',
    'INGLES':                           'Inglés',
    'EDUCACION FISICA':                 'Educación Física',
    'ETICA':                            'Ética',
    'CULTURA CLASICA':                  'Cultura clásica',
    'MUSICA':                           'Música',
    'TECNOLOGIA':                       'Tecnología',
    'EDUCACION PLASTICA':               'Educación Plástica',
    'FRANCES':                          'Francés',
}


def main():
    # pandas tiene el metodo read_excel y recibe 2 parametros, 1-nombre hoja, 2-sheet_name= refiere a la hoja
    excel_df = pd.read_excel(NOTAS_ALUMNOS_PATH, sheet_name='Notas')
    # tomamos la posicion y las filas y a cada fila tomamos solo la de nombre
    for index, row in excel_df.iterrows():
        print(index, row['NOMBRE'])

    # drop_duplicates elimina las repetidas para solo tomar 1 de cada 1 - pandas entrega una serie asi que con list lo convertimos
    # variable = ordenar(convertir_a_lista(excel['columna'].eliminar_duplicado()))
    asig_list = sorted(list(excel_df['ASIGNATURA'].drop_duplicates()))
    print('asig_list', asig_list)

    # PASAR LOS VALORES DEL DICCIONARIO SEGUN EL EXCEL A LA LISTA
    filter_td_asig = [] # esta sera la lista ordenada con tildes
    for item in asig_list: # iteramos la columna asignatura del excel
        valorTd = dict_asig[item] # almacenar = diccionario[valor]
        filter_td_asig.append(valorTd)
    print('')




if __name__ == '__main__':
    main()