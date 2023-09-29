import pandas as pd  # manipulacion y analisis de datos
import sys  # funcionalidades relacionadas al sistema operativo  #estandar
import shutil  # manipulacion de archivos y directorios como copiar, mover, elimnar, etc   #estadar
import os  # interactuar con el sistema operativo subyacente, util para archivos, directorios y rutas  #estandar
from docxtpl import DocxTemplate  # manipular word => docxtemplate trabaja con el contexto
import copy  # copia de objetos complejos #estandar
# aunque no se importe se necesita instalar openpyxl


#Corresponde a nuestro excel de alumnos
NOTAS_ALUMNOS_PATH = r'inputs/Notas_Alumnos.xlsx'
#Corresponde a nuestro word de cursos
PLANTILLA_CURSOS_PATH = r'inputs/Plantilla_Notas.docx'
# corresponde a los archivos creados
PATH_OUTPUT = r'.\out'
# fecha cursos
CURSO = '2021/2022'
# Colores
SUSPENSO_COLOR = 'ec7c7b'
APROBADO_COLOR = 'fbe083'
NOTABLE_COLOR = '4db4d7'
SOBRESALIENTE_COLOR = '48bf91'

dict_asig = {
        'LENGUA CASTELLANA Y LITERATURA': 'Lengua Castellana y Literatura',
        'BIOLOGIA': 'Biología',
        'GEOGRAFIA E HISTORIA': 'Geografía e Historia',
        'MATEMATICAS': 'Matemáticas',
        'INGLES': 'Inglés',
        'EDUCACION FISICA': 'Educación Física',
        'ETICA': 'Ética',
        'CULTURA CLASICA': 'Cultura clásica',
        'MUSICA': 'Música',
        'TECNOLOGIA': 'Tecnología',
        'EDUCACION PLASTICA': 'Educación Plástica',
        'FRANCES': 'Francés',
    }

# validar errores
def deteccionErrores(df):
    err1, err2, err3 = False, False, False

    # variable = ordenar(convertir_a_lista(dataframe['columna'].eliminar_duplicado()))
    alumnos_list = sorted(list(df['NOMBRE'].drop_duplicates()))
    asignatura_list = sorted(list(df['ASIGNATURA'].drop_duplicates()))


    for al in alumnos_list: # recorremos lista de alumnos
        for asig in asignatura_list: # este doble ciclo se entenderia como tomar todos los alumnos y cada alumno todas sus asignaturas "materias"
            # en cada ciclo comparamos del dataframe el alumno y en el ciclo anidado comparamos cada materia y asignara cada que al y asig sean igual
            filt_al_as_df = df[(df['NOMBRE'] == al) & (df['ASIGNATURA'] == asig)]

            if(len(filt_al_as_df) == 0):
                print(f'Error: El alumno {al} no tiene la asignatura {asig} asignada')
                err1 = True

            elif(len(filt_al_as_df) > 1):
                print(f'Error: El alumno {al} tiene la asignatura {asig} repetida {len(filt_al_as_df)} veces')
                err2 = True

        for index, row in df.iterrows(): # recorrer dataframe
            trimestre_list = ['NOTA T1', 'NOTA T2', 'NOTA T3']
            for trim in trimestre_list: #sobre cada iteracion del dataframe iteramos las notas
                # row[trim] -> row = head de la columna --- trim valor que tiene el head de la columna ejemplo NOTA 1
                if not((row[trim] >= 0.0) and (row[trim] <=10.0)): # validamos que cada nota no exceda 10.0 ni 0.0
                    print(f'Error: El alumno {al} tiene el campo {trim} de la asginatura {asig}  fuera de rango {str(row[trim])}')
                    err3 = True

    if (err1 == True ) or (err2 == True) or (err3 == True):
        print('')
        print('Debes corregir los errores para continuar con la ejecucion del programa')
        sys.exit(1) # 1 error, 0 exitoso
    else:
        print('Ningun error detectado ')


# elimina carpeta out y vuelve a crearla
def eliminarCrearCarpetas(path):
    if os.path.exists(path): # valida si existe esa carpeta
        shutil.rmtree(path)  # elimina la carpeta

    os.mkdir(path)           # crea de nuevo una carpeta con el mismo nombre


# Funcion para eliminar tildes
def eliminarTildes(texto):

    tildes_dict = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
    }

    # esto si es necesario ya que si intentara solo definir y en el replace poner texto este valor se reiniciaria porque siempre estaria cambiando cada tilde del valor inicial
    # y solo entregaria el valor cambiado de las "U"
    textoSinTilde = texto

    # recorremos diccionario y 
    for key in tildes_dict: 
        # textofinal = textoIterado.cambiar("letraConTilde", diccionario[letraSinTilde])  -- interpretacion clara
        textoSinTilde = textoSinTilde.replace(key, tildes_dict[key])

    return textoSinTilde # resultado despues de todas las iteraciones


# nota final
def ObtenerNotaFinal(dict_asignatura):
    newAsignaturaDic = copy.deepcopy(dict_asignatura) # crea una copia de la variable
    TRIMESTRE_LIST = ['t1', 't2', 't3'] # se recorrera para sacar la media


    #Obtener la nota final
    nota_media = 0
    for trim in TRIMESTRE_LIST:
        nota_media += newAsignaturaDic[trim]
    nota_media /= 3
    newAsignaturaDic['nota_final'] = round(nota_media, 1)


    #Obtenemos la calificacion
    if(nota_media < 5.0):
        calif = 'SUSPENSO'
        color_calif = SUSPENSO_COLOR
    elif (nota_media < 7.0):
        calif = 'APROBADO'
        color_calif = APROBADO_COLOR
    elif (nota_media < 9.0):
        calif = 'NOTABLE'
        color_calif = NOTABLE_COLOR
    else:
        calif = 'SOBRESALIENTE'
        color_calif = SOBRESALIENTE_COLOR
    newAsignaturaDic['calificacion'] = calif
    newAsignaturaDic['color'] = color_calif

    return newAsignaturaDic


# crear word con tags asignados
def crearWordAsignarTag(datos_alumnos, excel_df):
    # drop_duplicates elimina las repetidas para solo tomar 1 de cada 1 - pandas entrega una 'serie' asi que con la funcion list lo convertimos
    # variable = ordenar(convertir_a_lista(excel['columna'].eliminar_duplicado()))
    asig_list = sorted(list(excel_df['ASIGNATURA'].drop_duplicates()))

    # PASAR LOS VALORES DEL DICCIONARIO SEGUN EL EXCEL A LA LISTA
    filter_td_asig = [] # esta sera la lista ordenada con tildes
    for item in asig_list: # iteramos la columna asignatura del excel
        valorTd = dict_asig[item] # almacenar = diccionario[valor]
        filter_td_asig.append(valorTd.upper()) # agregamos a la lista el valor del diccionario

    # recorre con lista de alumnos
    nombre_Alumno_list = sorted(list(datos_alumnos['NOMBRE']))  # lista con todos los nombres
    for nombre_alumno in nombre_Alumno_list: #por cada nombre hacemos este recorrido
        # Cargar documento plantilla
        docs_tpl = DocxTemplate(PLANTILLA_CURSOS_PATH) # parametro es el path

        filt_datos_alumnos_df = datos_alumnos[(datos_alumnos['NOMBRE'] == nombre_alumno)] # cogemos todos los datos del alumno que se esta recorriendo

        clase = filt_datos_alumnos_df.iloc[0]['CLASE'] # iloc recorre celdas iloc[fila][columna]

        #Crear TABLA de notas word
        asignatura_list = []
        #Iterar sobre los indices de asignaturas
        for asig_idx in range(len(asig_list)):
            asign = asig_list[asig_idx] # la variable es la asignacion
            filt_al_as_excel_df = excel_df[(excel_df['NOMBRE'] == nombre_alumno) & (excel_df['ASIGNATURA'] == asign)]

            asignatura_dict = {
                'nombre_asignatura': filter_td_asig[asig_idx],
                't1': round(filt_al_as_excel_df.iloc[0]['NOTA T1'],1),
                't2': round( filt_al_as_excel_df.iloc[0]['NOTA T2'],1),
                't3': round(filt_al_as_excel_df.iloc[0]['NOTA T3'],1),
            }
            asignatura_dict = ObtenerNotaFinal(asignatura_dict)

            asignatura_list.append(asignatura_dict)



        #Context   -> son las variables del archivo word - clave=nombre variable en word - valor=valor a entregar en el excel
        context = {
            'curso': CURSO,
            'nombre_alumno': nombre_alumno,
            'clase': clase,
            'asignatura_list': asignatura_list,
        }

        #Renderizamos el documento word
        docs_tpl.render(context)  # docs_tpl es el archivo word, renderizamos con el contexto creado asignando asi las variables
        # titulo = 'NOTAS_' + nombre_alumno
        # titulo = titulo.upper()
        # titulo = eliminarTildes(titulo)
        # titulo = titulo.replace(" ", "_")
        # titulo += '.docx'
        # todos los titulos los cambiaria por la siguiente forma, aunque reconozco que seria mas dificil de leer
        titulo = eliminarTildes(f"NOTAS_{nombre_alumno.upper()}.docx").replace(" ", "_")

        docs_tpl.save(PATH_OUTPUT + '\\' + titulo) # aqui se guarda el documento


# funcion principal
def main():
    eliminarCrearCarpetas(PATH_OUTPUT)  # si existe la carpeta la elimina, y la crea de nuevo vacia

    #Leemos notas y datos alumnos
    # pandas tiene el metodo read_excel y recibe 2 parametros, 1-ruta archivo, 2-sheet_name= refiere al nombre de la hoja
    excel_df = pd.read_excel(NOTAS_ALUMNOS_PATH, sheet_name='Notas') # hoja 1 notas
    datos_alumnos = pd.read_excel(NOTAS_ALUMNOS_PATH, sheet_name='Datos_Alumnos') # hoja 2 datos alumnos

    # tomamos la posicion y las filas y a cada fila tomamos solo la de nombre
    # esto solo era para leer la informacion
    # for index, row in excel_df.iterrows():
    #     print(index, row['NOMBRE'])

    #Detectamos errores
    deteccionErrores(excel_df)

    #Creamos y asignamos tags en el word
    crearWordAsignarTag(datos_alumnos, excel_df)


# ejecuta la funcion main
if __name__ == '__main__':
    main()